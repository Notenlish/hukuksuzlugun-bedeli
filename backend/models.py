from enum import Enum

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


class UserPermission(str, Enum):
    USER = "normal"
    ADMIN = "admin"


class CategoryEnum(str, Enum):  # why is this not used anywhere?
    ECONOMY = "economy"
    CENSORSHIP = "censorship"


# --- Models --- #


class Account(models.Model):
    id = fields.IntField(primary_key=True)
    email = fields.CharField(max_length=255, unique=True)
    name = fields.CharField(max_length=50)
    lastname = fields.CharField(max_length=50)
    password = fields.CharField(max_length=255)

    role = fields.CharEnumField(UserPermission, default=UserPermission.USER)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    def __str__(self):
        return f"Account: {self.name} {self.lastname}"


class TrackedMetric(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, unique=True)
    description = fields.TextField(null=True)

    category = fields.CharField(max_length=255, null=True)  # TODO: change this to CategoryEnum
    source = fields.CharField(max_length=255, null=True)
    evds_code = fields.CharField(max_length=255, null=True)
    url = fields.CharField(max_length=255, null=True)
    unit = fields.CharField(max_length=255, null=True)

    data_type = fields.CharEnumField(DataTypeEnum, default=DataTypeEnum.numeric)
    frequency = fields.CharEnumField(FrequencyEnum, default=FrequencyEnum.DAILY)

    datapoints: fields.ReverseRelation["MetricDataPoint"]
    
    def __str__(self) -> str:
        return f"<TrackedMetric name:{self.name} category:{self.category} source:{self.source} evds_code:{self.evds_code} >"


class MetricDataPoint(models.Model):
    id = fields.IntField(pk=True)
    metric = fields.ForeignKeyField(
        "models.TrackedMetric", related_name="datapoints"
    )
    date = fields.DateField()

    value = fields.FloatField(null=True)  # if value
    value_text = fields.TextField(null=True)  # if text

    class Meta:  # pyright: ignore
        unique_together = ("metric", "date")
