from datetime import date
import os

import dotenv
import evdsclient

dotenv.load_dotenv(".env")

EVDS_API_KEY = os.environ["TCMB_EVDS2_API_KEY"]

class Fetcher:
    def __init__(self) -> None:
        self.evds = evdsclient.evdsAPI(EVDS_API_KEY)
        self.date_imamoglu_arrested = date(2025, 2, 19)  # 19 mart 2025

    def _get_past_data(self,type):
        today = date.today()
        df = self.evds.get_data([""])

        if df is None:
            raise Exception("df is none!")
        if df.empty:
            raise ValueError("No data for df")
print(df)
value = df.iloc[0, 1]  # Second column is the USD rate
print(value)

def start_scheduler():
    ...
