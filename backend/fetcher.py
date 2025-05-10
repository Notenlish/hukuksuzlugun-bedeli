import os

import dotenv
import evdsclient

dotenv.load_dotenv(".env")

EVDS_API_KEY = os.environ["TCMB_EVDS2_API_KEY"]

# Initialize client
evds = evdsclient.evdsAPI(EVDS_API_KEY)

df = evds.get_data(['TP.DK.USD.A'], startdate="02-01-2019", enddate="02-01-2023")
if df is None:
    raise Exception("df is none!")
if df.empty:
    raise ValueError("No data for df")
print(df)
value = df.iloc[0, 1]  # Second column is the USD rate
print(value)

def start_scheduler():
    ...
