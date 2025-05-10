from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import dotenv

dotenv.load_dotenv(".env")

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://user:password@your-neon-db.neon.tech/dbname")

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    from models import TrackedMetric, MetricDataPoint
    Base.metadata.create_all(bind=engine)
