import enum


class Aggregation(enum.StrEnum):
    AVG = "avg"
    MIN = "min"
    MAX = "max"
    FIRST = "first"
    LAST = "last"
    SUM = "sum"


class Formula(enum.StrEnum):
    PERCENTAGE_CHANGE = "1"
    DIFFERENCE = "2"
    YEARLY_PERCENTAGE_CHANGE = "3"
    YEARLY_DIFFERENCE = "4"
    PERCENTAGE_CHANGE_COMPARED_TO_END_OF_PREVIOUS_YEAR = "5"
    DIFFERENCE_COMPARED_TO_END_OF_PREVIOUS_YEAR = "6"
    MOVING_AVERAGE = "7"
    MOVING_TOTAL = "8"


class FrequencyEVDS(enum.StrEnum):
    daily = "1"
    workday = "2"
    weekly = "3"
    twice_a_month = "4"
    monthly = "5"
    quarterly = "6"
    six_months = "7"
    yearly = "8"


class DataType(enum.StrEnum):
    NUMERIC = "numeric"
    PERCENT = "percent"


"""
"MONTHLY_PPI": {
    "name": "Producer Price Index (PPI)",
    "code": "TP.FG.UFE",
    "unit": "index",
    "frequency": EVDSFrequencyMap[FrequencyEnum.MONTHLY.value],
    "data_type": DataType.NUMERIC,
    "category": "economy",
    "description": "Monthly producer inflation (PPI)",
},
"""
