import enum
from datetime import date

from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.types import Date, Float, Integer, String

Base = declarative_base()

# SQL Models


# custom data types for tracking data
class DataTypeEnum(str, enum.Enum):
    numeric = "numeric"
    boolean = "boolean"
    text = "text"
    percent = "percent"


class FrequencyEnum(str, enum.Enum):
    hourly = "hourly"
    daily = "daily"
    monthly = "monthly"
    realtime = "realtime"
    ad_hoc = "ad_hoc"


class DataSourceEnum(str, enum.Enum):
    EVDS = "evds"
    SCRAPER = "scraper"
    # ... to be added


class CategoryEnum(str, enum.Enum):
    ECONOMY = "economy"
    CENSHORSHIP = "censorship"


class TrackedMetric(Base):
    __tablename__ = "tracked_metrics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)

    category = Column(String, nullable=True)
    source = Column(String, nullable=True)
    evds_code = Column(String, nullable=True)  # If from EVDS
    url = Column(String, nullable=True)  # API or Scraping source
    unit = Column(String, nullable=True)

    data_type = Column(SqlEnum(DataTypeEnum), default=DataTypeEnum.numeric)
    frequency = Column(SqlEnum(FrequencyEnum), default=FrequencyEnum.daily)

    datapoints = relationship("MetricDataPoint", back_populates="metric")


class MetricDataPoint(Base):
    __tablename__ = "metric_data_points"

    id = Column(Integer, primary_key=True, index=True)
    metric_id = Column(Integer, ForeignKey("tracked_metrics.id"), nullable=False)
    date = Column(Date, nullable=False)

    value = Column(Float, nullable=True)  # for numeric or percent
    value_text = Column(String, nullable=True)  # for string or boolean types

    metric = relationship("TrackedMetric", back_populates="datapoints")

    __table_args__ = (UniqueConstraint("metric_id", "date", name="unique_metric_date"),)


# --- Pydantic Models --- #


class MetricBase(BaseModel):
    name: str
    description: str | None
    source: str | None
    evds_code: str | None
    url: str | None
    unit: str | None
    category: str | None
    data_type: DataTypeEnum
    frequency: FrequencyEnum


class DataPointBase(BaseModel):
    date: date
    value: float | None
    value_text: str | None
    metric_id: int
