from models import Base, TrackedMetric, MetricDataPoint
from db import engine

# This will create all tables defined in models.py
Base.metadata.create_all(bind=engine)

print("Database initialized.")
