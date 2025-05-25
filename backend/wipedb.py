from db import init_db
from tortoise import Tortoise, run_async
from fetcher import Fetcher
from models import TrackedMetric, MetricDataPoint

async def _():
    await init_db()
    Tortoise.get_connection("default")
    
    await MetricDataPoint.all().delete()
    await TrackedMetric.all().delete()

if __name__ == '__main__':
    run_async(_())