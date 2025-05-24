import enum
import os
from datetime import date, datetime
from typing import TypedDict

import dotenv
import evdsclient
from evds_series import Aggregation, FrequencyEVDS
from models import DataTypeEnum, FrequencyEnum, MetricDataPoint, TrackedMetric
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
    category: str
    description: str


EVDS_SERIES: dict[str, EVDSSeriesMeta] = {
    "DAILY_USD_TRY": {
        "name": "USD/TRY Exchange Rate",
        "code": "TP.DK.USD.A",
        "unit": "TRY",
        "frequency": FrequencyEnum.DAILY,
        "data_type": DataType.NUMERIC,
        "category": "economy",
        "description": "Daily exchange rate of USD to TRY",
    },
}


class Fetcher:
    def __init__(self) -> None:
        print("starting up...")
        self.evds = evdsclient.evdsAPI(EVDS_API_KEY)
        print("created evds client")
        self.date_imamoglu_arrested = date(2025, 2, 19)  # 19 mart 2025

    async def populate_db_with_past_evds_data(self):
        print("created session")
        today = date.today()

        for key, meta in EVDS_SERIES.items():
            # df yi niye kullanıyorum ki bozuk zaten
            df = self.evds.get_data(
                series=[meta["code"]],
                startdate=self.date_imamoglu_arrested,
                enddate=today,
                aggregation_types=Aggregation.AVG,
                formulas="",
                frequency=meta["frequency"],
            )
            print("Bu niye çalışıyor!?!?\n", df)
            if df is None or df.empty:
                print(f"No data for {key}!")
                continue

            # TP.DK.USD.A -> DP_DK_USD_A
            column_name = meta["code"].replace(".", "_")

            df[column_name] = df[
                column_name
            ].ffill()  # get rid of NaN for holidays, replace with the last available value

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

            print(result)
            for index, series_data in result[1:].iterrows():
                print(series_data)
                date_str = series_data["Tarih"]  # dd-mm-yyyy
                if not isinstance(date_str, str):
                    raise TypeError("date_str is not string")

                value = series_data[column_name]

                print("datestr", date_str, "value", value)

                old_datapoint = MetricDataPoint.filter(metric=metric, date=datetime.strptime(date_str, "%d-%m-%Y").date()).first()
                if old_datapoint is None: # doesnt exist yet
                    datapoint = MetricDataPoint(
                        metric=metric,
                        date=datetime.strptime(date_str, "%d-%m-%Y").date(),
                        value=value,
                    )
                    await datapoint.save()
                else:
                    pass  # no need to create another one or update. 


def start_scheduler(): ...


if __name__ == "__main__":
    f = Fetcher()

    async def _():
        await f.populate_db_with_past_evds_data()

    k = _()
