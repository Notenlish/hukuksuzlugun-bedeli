from enum import Enum
from datetime import date
from tortoise import fields, models


# --- Enums --- #
class DataTypeEnum(str, Enum):
    numeric = "numeric"
    boolean = "boolean"
    text = "text"
    percent = "percent"


class FrequencyEnum(str, Enum):
    DAILY = "daily"
    WORKDAY = "workday"
    WEEKLY = "weekly"
    TWICE_A_MONTH = "twice_a_month"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    SIX_MONTHS = "six_months"
    YEARLY = "yearly"


class DataSourceEnum(str, Enum):
    EVDS = "evds"
    SCRAPER = "scraper"


class CategoryEnum(str, Enum):
    ECONOMY = "economy"
    CENSHORSHIP = "censorship"

# --- Models --- #
class TrackedMetric(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, unique=True)
    description = fields.TextField(null=True)

    category = fields.CharField(max_length=255, null=True)
    source = fields.CharField(max_length=255, null=True)
    evds_code = fields.CharField(max_length=255, null=True)
    url = fields.CharField(max_length=255, null=True)
    unit = fields.CharField(max_length=255, null=True)

    data_type = fields.CharEnumField(DataTypeEnum, default=DataTypeEnum.numeric)
    frequency = fields.CharEnumField(FrequencyEnum, default=FrequencyEnum.DAILY)

    datapoints: fields.ReverseRelation["MetricDataPoint"]


class MetricDataPoint(models.Model):
    id = fields.IntField(pk=True)
    metric = fields.ForeignKeyField("models.TrackedMetric", related_name="datapoints")
    date = fields.DateField()

    value = fields.FloatField(null=True)
    value_text = fields.TextField(null=True)

    class Meta: # pyright: ignore
        unique_together = ("metric", "date")
