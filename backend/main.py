from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from db import init_db,close_db

from fetcher import start_scheduler
from models import MetricDataPoint, TrackedMetric, Account
from settings import TORTOISE_ORM
from tortoise.contrib.fastapi import register_tortoise


app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=False,  # Set to True if you don't want to use aerich and use tortoise for generating schemas.
    add_exception_handlers=True,
)


@app.on_event("startup")
async def startup():
    await init_db()
    # init_db()
    # start_scheduler()

@app.on_event("shutdown")
async def on_shutdown():
    await close_db()

"/api/metrics"
"/api/datapoints"
