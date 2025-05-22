from datetime import date, datetime
from enum import Enum
from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from tortoise import Tortoise

from db import init_db, close_db
from contextlib import asynccontextmanager
import os
from pprint import pprint


from fetcher import start_scheduler
from models import MetricDataPoint, TrackedMetric, Account
from settings import TORTOISE_ORM
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
async def viewdb(include_data: bool = Query(False, description="Set to true to include data from tables")):
    """
        Development endpoint to view database tables and optionally their data.
        WARNING: DO NOT USE IN PRODUCTION.
    """
    if os.getenv("ENV") == "production":
        return JSONResponse(
            status_code=403,
            content={"error": "This endpoint is not available in production environment."},
        )
    
    try:
        # Get the default connection
        conn = Tortoise.get_connection("default")
        
        models_app = Tortoise.apps.get("models")
        if not models_app:
            return {"error":"Models app not found or not initialized."}
        table_names_and_data = {}
        only_table_names = []
        
        for model_name, model_class in models_app.items():
            if not hasattr(model_class, "_meta") or not hasattr(model_class._meta, "db_table"):
                # This might happen for base classes or non-table models if any are registered
                continue
            
            table_name = model_class._meta.db_table
            only_table_names.append(table_name)
            
            column_names = [d["db_column"] for d in model_class.describe()["data_fields"]]
            
            if include_data:
                try:
                    # fetch all records from the model
                    records = await model_class.all()
                    serialized = []
                    for record in records:
                        record_data = {}
                        # Iterate over the model's fields to build a dictionary
                        for field_name in record._meta.fields_map.keys():
                            value = getattr(record, field_name)
                            # Basic serialization for common types
                            if isinstance(value, (datetime, date)):
                                record_data[field_name] = value.isoformat()
                            elif isinstance(value, Enum):
                                record_data[field_name] = value.value
                                # get the primitive value of the enum.
                                # I might need to update this to handle more complex types 
                            else:
                                record_data[field_name] = value
                        serialized.append(record_data)
                    table_names_and_data[table_name] = {"records":serialized,"columns":column_names}
                except Exception as e:
                    table_names_and_data[table_name] = {"error": f"Could not fetch data for {table_name}: {str(e)}"}
        if include_data:
            return table_names_and_data
        else:
            return {"tables": only_table_names}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"An error occurred while accessing database schema/data: {str(e)}"}
        )

# start_scheduler()

"/api/metrics"
"/api/datapoints"
