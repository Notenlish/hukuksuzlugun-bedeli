import enum
import os
from datetime import date
from typing import TypedDict

import dotenv
import evdsclient
from evds_series import Aggregation
from models import (
    FrequencyEnum,
    TrackedMetric,
)

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

    def populate_db_with_past_evds_data(self):
        today = date.today()
        print("created session")

        for key, meta in EVDS_SERIES.items():
            df = self.evds.get_data(
                series=[meta["code"]],
                startdate=self.date_imamoglu_arrested,
                enddate=today,
                aggregation_types=Aggregation.AVG,
                formulas="",
                frequency=meta["frequency"],
            )
            if df is None or df.empty:
                print(f"No data for {key}!")
                continue

            # TP.DK.USD.A -> DP_DK_USD_A
            column_name = meta["code"].replace(".", "_")

            df[column_name] = df[
                column_name
            ].ffill()  # get rid of NaN for holidays, replace with the last available value

            ###

            metric = TrackedMetric.filter(evds_code=meta["code"]).first

            """if not metric:
                metric = TrackedMetric(
                    name=meta["name"],
                    description=meta["description"],
                    source="evds",
                    evds_code=meta["code"],
                    url=None,
                    unit=meta["unit"],
                    category=meta["category"],
                    data_type=DataTypeEnum(meta["data_type"]),
                    frequency=FrequencyEnum(meta["frequency"])
                )
                session.add(metric)
                session.commit()
                session.refresh(metric)"""


def start_scheduler(): ...


if __name__ == "__main__":
    f = Fetcher()
    f.populate_db_with_past_evds_data()
