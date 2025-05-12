from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from db import get_db

from fetcher import start_scheduler
from models import MetricDataPoint, TrackedMetric, DataPointBase, MetricBase
from sqlalchemy.orm import Session


app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    # init_db()
    start_scheduler()


@app.get("/api/metrics", response_model=list[MetricBase])
def get_metrics(db: Session = Depends(get_db)):
    return db.query(TrackedMetric).all()


@app.get("/api/datapoints", response_model=list[DataPointBase])
def get_datapoints(db: Session = Depends(get_db)):
    return db.query(MetricDataPoint).all()
