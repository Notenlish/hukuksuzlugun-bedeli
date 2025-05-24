from db import init_db
from tortoise import Tortoise, run_async
from fetcher import Fetcher

async def _():
    await init_db()
    Tortoise.get_connection("default")

    fetcher = Fetcher()
    await fetcher.fetch_inflation()
    #await fetcher.populate_db_with_past_evds_data()

run_async(_())