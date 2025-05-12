from datetime import date
import os

import dotenv
import evdsclient
from evds_series import EVDS_SERIES, Aggregation

from db import SessionLocal
from models import (
    TrackedMetric,
    MetricDataPoint,
    DataTypeEnum,
    FrequencyEnum,
    DataSourceEnum,
)

dotenv.load_dotenv(".env")

EVDS_API_KEY = os.environ["TCMB_EVDS2_API_KEY"]


class Fetcher:
    def __init__(self) -> None:
        self.evds = evdsclient.evdsAPI(EVDS_API_KEY)
        self.date_imamoglu_arrested = date(2025, 2, 19)  # 19 mart 2025

    def populate_db_with_past_evds_data(self):
        today = date.today()
        session = SessionLocal()

        try:
            for key, meta in EVDS_SERIES.items():
                df = self.evds.get_data(
                    series=[meta["code"]],
                    startdate=self.date_imamoglu_arrested,
                    enddate=today,
                    aggregation_types=Aggregation.AVG,
                    formulas="",
                    frequency=meta["frequency"],
                    raw=False,
                )
                if df is None or df.empty:
                    print(f"No data for {key}!")
                    continue

                # TP.DK.USD.A -> DP_DK_USD_A
                column_name = meta["code"].replace(".", "_")

                df[column_name] = df[
                    column_name
                ].ffill()  # get rid of NaN for holidays, replace with the last available value

                # Create or fetch the TrackedMetric
                metric = (
                    session.query(TrackedMetric)
                    .filter_by(evds_code=meta["code"])
                    .first()
                )
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
                        frequency=FrequencyEnum(meta["frequency"])
                    )
                    session.add(metric)
                    session.commit()
                    session.refresh(metric)

                for _, row in df.iterrows():
                    datapoint_date=row["Tarih"]
                    value=row[column_name]
                    
                    # Avoid duplicate (unique on metric_id + date)
                    exists = session.query(MetricDataPoint).filter_by(
                        metric_id=metric.id,
                        date=datapoint_date
                    ).first()
                    if exists:
                        continue
                    
                    datapoint = MetricDataPoint(
                        metric_id=metric.id,
                        date=datapoint_date,
                        value=value if meta["data_type"] == "numeric" or meta["data_type"] == "percent" else None,
                        value_text=str(value) if meta["data_type"] not in ("numeric", "percent") else None
                    )
                    session.add(datapoint)
                session.commit()
                print(f"Inserted data for: {key}")
        finally:
            session.close()


def start_scheduler(): ...


if __name__ == "__main__":
    f = Fetcher()
    f.populate_db_with_past_evds_data()
