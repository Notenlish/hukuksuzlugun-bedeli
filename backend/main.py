import os
from contextlib import asynccontextmanager
from datetime import date, datetime
from enum import Enum

from db import close_db, init_db
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from settings import TORTOISE_ORM
from tortoise import Tortoise, fields
from tortoise.contrib.fastapi import register_tortoise


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("starting api")
    await init_db()

    yield

    print("shutting down api")

    await close_db()
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


@app.get("/viewdb")
async def viewdb_endpoint(
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
                            # print("!!! getting field names", field_name)
                            value = getattr(record, field_name)
                            # print("!----! field value:", value)

                            # Basic serialization for common types
                            if isinstance(value, (datetime, date)):
                                record_data[field_name] = value.isoformat()
                            elif isinstance(value, Enum):
                                record_data[field_name] = value.value  # get the primitive value of the enum.
                            elif isinstance(value, fields.ReverseRelation):
                                related_ids = []  # serialize as a list of ID's
                                async for related_obj in value: # ReverseRelation is an awaitable queryset
                                    related_ids.append(related_obj.pk) # Assuming 'pk' is the primary key
                                record_data[field_name] = related_ids
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
