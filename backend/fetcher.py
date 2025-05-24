import enum
import os
import time
from datetime import date, datetime, timedelta
from typing import TypedDict

import dotenv
import evdsclient
from evds_series import FrequencyEVDS
from models import (
    CategoryEnum,
    DataTypeEnum,
    FrequencyEnum,
    MetricDataPoint,
    TrackedMetric,
)
from pandas import DataFrame

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


class Fetcher:
    def __init__(self) -> None:
        print("starting up...")
        self.evds = evdsclient.evdsAPI(EVDS_API_KEY)
        print("created evds client")
        self.date_imamoglu_arrested = date(2025, 2, 19)  # 19 mart 2025

    async def do_scheduled_task(self):
        today = date.today()
        start = today - timedelta(days=2)
        end = today

        await self.do_evds_stuff(EVDS_SERIES, start, end)

    async def do_evds_stuff(
        self, evds_series_data: dict[str, EVDSSeriesMeta], start: date, end: date
    ):
        for key, meta in evds_series_data.items():
            # df yi niye kullanıyorum ki bozuk zaten
            # df = self.evds.get_data(
            #    series=[meta["code"]],
            #    startdate=self.date_imamoglu_arrested,
            #    enddate=today,
            #    aggregation_types=Aggregation.AVG,
            #    formulas="",
            #    frequency=meta["frequency"],
            # )

            # TP.DK.USD.A -> DP_DK_USD_A
            column_name = meta["code"].replace(".", "_")

            metric = await TrackedMetric.filter(evds_code=meta["code"]).first()

            if not metric:
                metric = TrackedMetric(
                    name=meta["name"],
                    description=meta["description"],
                    source="evds",
                    evds_code=meta["code"],
                    url=None,
                    unit=meta["unit"],
                    category=meta["category"],
                    data_type=DataTypeEnum(meta["data_type"]),
                    frequency=FrequencyEnum(meta["frequency"]),
                )
                await metric.save()
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

            result.ffill(inplace=True)

            # print(result)
            for index, series_data in result[1:].iterrows():
                # print(series_data)

                strp_format = "%d-%m-%Y"
                if metric.frequency == FrequencyEnum.MONTHLY:
                    strp_format = "%Y-%m"  # yyyy-m (month isnt zero padded)

                date_str = series_data["Tarih"]  # dd-mm-yyyy
                if not isinstance(date_str, str):
                    raise TypeError("date_str is not string")

                value = series_data[column_name]

                # print("datestr", date_str, "value", value)

                old_datapoint = MetricDataPoint.filter(
                    metric=metric, date=datetime.strptime(date_str, strp_format).date()
                ).first()
                if old_datapoint is None:  # doesnt exist yet
                    datapoint = MetricDataPoint(
                        metric=metric,
                        date=datetime.strptime(date_str, "%d-%m-%Y").date(),
                        value=value,
                    )
                    await datapoint.save()
                else:
                    pass  # no need to create another one or update.

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
