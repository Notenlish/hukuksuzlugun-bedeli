import os
from contextlib import asynccontextmanager
from datetime import date, datetime, timedelta
from enum import Enum
from dotenv import load_dotenv

print("Loading .env file. Loading ENVIRONMENT VARIABLES.")

load_dotenv(".env")

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from db import close_db, init_db
from fastapi import Depends, FastAPI, HTTPException, Query, Security, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader
from fetcher import EVDS_SERIES, Fetcher
from models import DataTypeEnum, FrequencyEnum, MetricDataPoint, TrackedMetric
from settings import TORTOISE_ORM
from tortoise import Tortoise, fields, queryset
from tortoise.contrib.fastapi import register_tortoise
from utils import (
    first_day_of_current_month,
    first_day_of_the_previous_month,
    last_friday_on_or_before,
)

fetcher = Fetcher()

# Create a scheduler instance
# scheduler = BackgroundScheduler()  # for normal functions
scheduler = AsyncIOScheduler()


async def scheduled_fetch_task():
    print(f"Scheduled task executed at: {datetime.now()}")
    await fetcher.do_scheduled_task()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("starting api")
    await init_db()

    scheduler.add_job(
        scheduled_fetch_task, IntervalTrigger(hours=2), id="test_periodic_job"
    )
    scheduler.start()

    yield

    print("shutting down api")

    await close_db()

    print("Shutting down scheduler...")
    scheduler.shutdown()
    # nothing here, code after yield will be run on shutdown


app = FastAPI(lifespan=lifespan)

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

API_ACCESS_KEY = os.environ.get("API_ACCESS_KEY")

if not API_ACCESS_KEY:
    raise RuntimeError("API_ACCESS_KEY environment variable not set.")

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)


async def api_key_required(header_key: str = Security(api_key_header)):
    """For validating if the API key was provided in the header."""
    if header_key == API_ACCESS_KEY:
        return header_key

    # Key invalid
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API Key",
        headers={"X-API-Key": "Bearer"},
    )


@app.get("/ping")
async def public_endpoint():
    return JSONResponse(content={"message": "Pong!"})


@app.post("/get-change")
async def get_change_endpoint(api_key: str = Depends(api_key_required)):
    print("GET CHANGE ASDASDMASKDMLASLKDM")
    output = {}
    for key, value in EVDS_SERIES.items():
        metric = await TrackedMetric.filter(name=value["name"]).first()
        assert metric is not None

        freq = value["frequency"]

        if freq == FrequencyEnum.DAILY:
            startdate = fetcher.date_imamoglu_arrested
            enddate = date.today()
        elif freq==FrequencyEnum.WEEKLY:
            startdate = last_friday_on_or_before(fetcher.date_imamoglu_arrested)  # TODO: change this to date_imamoglu_arrested maybe?
            # lazy EVDS api lags behind and doesnt update data on schedule. F*ck you evds.
            enddate = last_friday_on_or_before(date.today() - timedelta(days=7))
        elif freq == FrequencyEnum.MONTHLY:
            startdate = first_day_of_current_month(
                fetcher.date_imamoglu_arrested
            )  # first_day_of_the_next_month(fetcher.date_imamoglu_arrested)
            enddate = first_day_of_the_previous_month(date.today())
        else:
            raise Exception(f"I haven't coded anything for this frequency: {freq}")

        # (2025, 3, 19) = date imamoglu arrested
        print(metric)
        print(startdate, enddate)

        start = await MetricDataPoint.filter(metric=metric, date=startdate).first()
        end = await MetricDataPoint.filter(metric=metric, date=enddate).first()
        

        if start is None or end is None:
            raise Exception(f"A value is null. start is {start} end is {end}.")
        
        print(start.value, end.value)

        if metric.data_type == DataTypeEnum.numeric:
            change_value = end.value - start.value
            change_perc = 100 * (change_value / start.value)
            output[key] = {
                "changeValue": change_value,
                "changePercentage": change_perc,
                "startValue": start.value,
                "endValue": end.value,
            }
        else:
            raise Exception(
                f"I haven't coded anything for this datatype: {metric.data_type}"
            )
    return JSONResponse(content=output)


@app.post("/viewdb")
async def viewdb_endpoint(
    api_key: str = Depends(api_key_required),
    include_data: bool = Query(
        False, description="Set to true to include data from tables"
    ),
):
    """
    Development endpoint to view database tables and optionally their data.
    WARNING: DO NOT USE IN PRODUCTION.
    """

    if os.getenv("ENV") == "production":
        return JSONResponse(
            status_code=403,
            content={
                "error": "This endpoint is not available in production environment."
            },
        )

    try:
        # Get the default connection
        conn = Tortoise.get_connection("default")  # noqa: F841

        models_app = Tortoise.apps.get("models")
        if not models_app:
            return {"error": "Models app not found or not initialized."}
        table_info_dict = {}
        table_names_list = []

        for model_name, model_class in models_app.items():
            if not hasattr(model_class, "_meta") or not hasattr(
                model_class._meta, "db_table"
            ):
                # This might happen for base classes or non-table models if any are registered
                continue

            table_name = model_class._meta.db_table
            table_names_list.append(table_name)

            column_names = [
                d["db_column"] for d in model_class.describe()["data_fields"]
            ]

            if include_data:
                try:
                    # fetch all records from the model
                    records = await model_class.all()
                    serialized = []
                    for record in records:
                        # print("!!!!!! will be alsdasdlasn records")
                        record_data = {}
                        # Iterate over the model's fields to build a dictionary
                        for field_name in record._meta.fields_map.keys():
                            value = getattr(record, field_name)

                            # Basic serialization
                            if isinstance(value, (datetime, date)):
                                record_data[field_name] = value.isoformat()
                            elif isinstance(value, Enum):
                                record_data[field_name] = (
                                    value.value
                                )  # get the primitive value of the enum.
                            elif isinstance(value, fields.ReverseRelation):
                                related_ids = []  # serialize as a list of ID's
                                async for (
                                    related_obj
                                ) in value:  # ReverseRelation is an awaitable queryset
                                    related_ids.append(
                                        related_obj.pk
                                    )  # Assuming 'pk' is the primary key
                                record_data[field_name] = related_ids
                            elif isinstance(value, queryset.QuerySet):
                                model = await value.all()
                                record_data[field_name] = model.pk  # type: ignore
                            else:
                                record_data[field_name] = value
                        # print("!!!!! Adding to serialized", record_data)
                        serialized.append(record_data)
                    table_info_dict[table_name] = {
                        "records": serialized,
                        "columns": column_names,
                    }
                except Exception as e:
                    table_info_dict[table_name] = {
                        "error": f"Could not fetch data for {table_name}: {str(e)}"
                    }
        if include_data:
            print("returning table names and data")
            print(table_info_dict)
            return table_info_dict
        else:
            return {"tables": table_names_list}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": f"An error occurred while accessing database schema/data: {str(e)}"
            },
        )


# start_scheduler()

"/api/metrics"
"/api/datapoints"
