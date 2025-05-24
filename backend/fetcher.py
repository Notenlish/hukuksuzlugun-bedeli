import enum
import os
import time
from datetime import date, datetime, timedelta
from typing import Any, TypedDict

import aiohttp
import dotenv
import evdsclient
from bs4 import BeautifulSoup
from evds_series import FrequencyEVDS
from models import (
    CategoryEnum,
    DataSourceEnum,
    DataTypeEnum,
    FrequencyEnum,
    MetricDataPoint,
    TrackedMetric,
)
from pandas import DataFrame, isna

dotenv.load_dotenv(".env")

EVDS_API_KEY = os.environ["TCMB_EVDS2_API_KEY"]


class DataType(enum.StrEnum):
    NUMERIC = "numeric"
    PERCENT = "percent"


class EVDSSeriesMeta(TypedDict):
    name: str
    code: str
    unit: str
    frequency: FrequencyEnum
    data_type: DataType
    category: CategoryEnum
    description: str


EVDS_SERIES: dict[str, EVDSSeriesMeta] = {
    "DAILY_USD_TRY": {
        "name": "USD/TRY Exchange Rate",
        "code": "TP.DK.USD.A",
        "unit": "TRY",
        "frequency": FrequencyEnum.DAILY,
        "data_type": DataType.NUMERIC,
        "category": CategoryEnum.ECONOMY,
        "description": "Daily exchange rate of USD to TRY",
    },
    "DAILY_EUR_TRY": {
        "name": "EUR/TRY Exchange Rate",
        "code": "TP.DK.EUR.A",
        "unit": "TRY",
        "frequency": FrequencyEnum.DAILY,
        "data_type": DataType.NUMERIC,
        "category": CategoryEnum.ECONOMY,
        "description": "Daily exchange rate of EUR to TRY",
    },
    "MONTHLY_CPI": {
        "name": "Consumer Price Index (CPI)",
        "code": "TP.FG.J0",
        "unit": "index",
        "frequency": FrequencyEnum.MONTHLY,
        "data_type": DataType.NUMERIC,
        "category": CategoryEnum.ECONOMY,
        "description": "Monthly inflation rate (CPI)",
    },
    # I got rid of the 10 year bond yield because EVDS doesnt give that data to me.
}

ENAG_DATA: dict[str, EVDSSeriesMeta] = {
    "INFLATION": {
        "name": "Monthly Inflation (ENAG)",
        "code": "",
        "unit": "%",
        "frequency": FrequencyEnum.MONTHLY,
        "data_type": DataType.PERCENT,
        "category": CategoryEnum.ECONOMY,
        "description": "Monthly inflation rate, calculated by ENAG.",
    }
}


class Fetcher:
    def __init__(self) -> None:
        print("starting up...")
        self.evds = evdsclient.evdsAPI(EVDS_API_KEY)
        print("created evds client")
        self.date_imamoglu_arrested = date(2025, 2, 19)  # 19 mart 2025

    async def fetch_inflation(self):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://enagrup.org/?hl=en") as response:
                # im giving up on making this readable, if it works it works.
                html = await response.text()
                soup = BeautifulSoup(html, features="html.parser")
                soup_text: str = soup.text
                _ = "The last 12 months increase rate in ENAGrup Consumer Price Index (E-CPI) is %"
                start = soup_text.find(_) + len(_)

                _ = "."
                end = start + soup_text[start:].find(_) + len(_)

                whole_part = soup_text[start:end].replace(".", "")

                l = end + soup_text[end:].find(_) + len(_)
                decimal_part = soup_text[end:l].replace(".", "")

                perc_inflation = float(f"{whole_part}.{decimal_part}")
        enag_inflation = ENAG_DATA["INFLATION"]
        metric = TrackedMetric.filter(source=DataSourceEnum.ENAG, name=enag_inflation).first()
        if not metric:
            metric = TrackedMetric(
                name=enag_inflation["name"],
                description=enag_inflation["description"],
                source=DataSourceEnum.ENAG,
                evds_code=enag_inflation["code"],
                url=None,
                unit=enag_inflation["unit"],
                category=enag_inflation["category"],
                data_type=DataTypeEnum(enag_inflation["data_type"]),
                frequency=FrequencyEnum(enag_inflation["frequency"]),
            )
            await metric.save()
        
        today = date.today()
        cur_month_date = date(year=today.year, month=today.month, day=1)  # always take the first day
        MetricDataPoint.filter(metric=metric, date=cur_month_date)  
        
        # I just realized the enag website gives the inflation data for february. It's may. Fuck.
        # Great I just spent god knows how long working on this just for it to be useless.
        # Why can't enag just provide an api
        # how hard could that be??

    async def do_scheduled_task(self):
        today = date.today()
        start = today - timedelta(days=2)
        end = today

        await self.do_evds_stuff(EVDS_SERIES, start, end)

    async def do_evds_stuff(
        self, evds_series_data: dict[str, EVDSSeriesMeta], start: date, end: date
    ):
        for key, meta in evds_series_data.items():
            # TP.DK.USD.A -> DP_DK_USD_A
            column_name = meta["code"].replace(".", "_")

            metric, created = await TrackedMetric.get_or_create(
                name=meta["name"],  # Use 'name' for lookup as it has the UNIQUE constraint
                defaults={  # These defaults are used ONLY if a new metric is created
                    "description": meta["description"],
                    "source": "evds",
                    "evds_code": meta["code"],
                    "url": None,
                    "unit": meta["unit"],
                    "category": meta["category"],
                    "data_type": DataTypeEnum(meta["data_type"]),
                    "frequency": FrequencyEnum(meta["frequency"]),
                }
            )
            if created:
                print(f"Created new metric: {metric.name} (EVDS Code: {metric.evds_code})")
            else:
                # TODO: I might need to make it update other parts too(if I change the EVDS_SERIES variable again)
                # If the metric already exists, ensure its evds_code is consistent
                # This handles cases where a name might match, but the evds_code might be different initially
                if metric.evds_code != meta["code"]:
                    print(f"Updating evds_code for existing metric '{metric.name}' from {metric.evds_code} to {meta['code']}")
                    metric.evds_code = meta["code"]
                    await metric.save() # Save the updated metric
                print(f"Using existing metric: {metric.name} (EVDS Code: {metric.evds_code})")
            print("METRIC BU ", metric)

            result: DataFrame | None = self.evds.get_data(
                [metric.evds_code],
                self.date_imamoglu_arrested,
                datetime.today().date(),
                aggregation_types="avg",
                frequency=FrequencyEVDS[metric.frequency].value,
            )
            if result is None:
                raise Exception("Couldn't fetch data.")
                # TODO: maybe just give a warning and continue?

            result.ffill(inplace=True)
            
            if 'Tarih' not in result.columns:
                print(f"Warning: 'Tarih' column not found in data for {metric.name}. Skipping.")
                continue

            print("!!!!!result",result)
            for index, series_data in result[1:].iterrows():
                print("---- series_data: ----\n",series_data)

                strp_format = "%d-%m-%Y"
                if metric.frequency == FrequencyEnum.MONTHLY:
                    strp_format = "%Y-%m"  # yyyy-m (month isnt zero padded)

                date_str = series_data["Tarih"]  # dd-mm-yyyy
                if not isinstance(date_str, str):
                    raise TypeError(f"date_str for {metric.name} is not a string. Type: {type(date_str)}")

                value = series_data.get(column_name)
                
                if value is None or isna(value):
                    print(f"Warning: Value for {metric.name} on {date_str} is missing or NaN. Skipping data point.")
                    continue
                
                try:
                    # Convert value to float if it's not already
                    value = float(value)
                except ValueError:
                    print(f"Warning: Could not convert value '{value}' for {metric.name} on {date_str} to float. Skipping.")
                    continue
                
                parsed_date = datetime.strptime(date_str, strp_format).date()

                datapoint, created_datapoint = await MetricDataPoint.get_or_create(
                    metric=metric,
                    date=parsed_date,
                    defaults={"value": value}
                )
                if created_datapoint:
                    print(f"Added data point for {metric.name} on {parsed_date} with value {value}")
                else:
                    if datapoint.value != value:
                        print(f"Updating data point for {metric.name} on {parsed_date} from {datapoint.value} to {value}")
                        datapoint.value = value
                        await datapoint.save()
                    else:
                        print(f"Data point for {metric.name} on {parsed_date} already exists with same value. Skipping update.")

            time.sleep(1)

    async def populate_db_with_past_evds_data(self):
        print("created session")
        today = date.today()

        await self.do_evds_stuff(EVDS_SERIES, self.date_imamoglu_arrested, today)


if __name__ == "__main__":
    f = Fetcher()

    async def _():
        await f.populate_db_with_past_evds_data()

    k = _()
