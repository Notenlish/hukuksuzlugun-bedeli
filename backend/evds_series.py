from typing import TypedDict
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


class Frequency(enum.StrEnum):
    DAILY = "1"
    WORKDAY = "2"
    WEEKLY = "3"
    TWICE_A_MONTH = "4"
    MONTHLY = "5"
    QUARTERLY = "6"
    SIX_MONTHS = "7"
    YEARLY = "8"


class DataType(enum.StrEnum):
    NUMERIC = "numeric"
    PERCENT = "percent"


class EVDSSeriesMeta(TypedDict):
    name: str
    code: str
    unit: str
    frequency: Frequency
    data_type: DataType
    category: str
    description: str


EVDS_SERIES: dict[str, EVDSSeriesMeta] = {
    "DAILY_USD_TRY": {
        "name": "USD/TRY Exchange Rate",
        "code": "TP.DK.USD.A",
        "unit": "TRY",
        "frequency": Frequency.DAILY,
        "data_type": DataType.NUMERIC,
        "category": "economy",
        "description": "Daily exchange rate of USD to TRY",
    },
    "DAILY_EUR_TRY": {
        "name": "EUR/TRY Exchange Rate",
        "code": "TP.DK.EUR.S.YTL",
        "unit": "TRY",
        "frequency": Frequency.DAILY,
        "data_type": DataType.NUMERIC,
        "category": "economy",
        "description": "Daily exchange rate of EUR to TRY",
    },
    "MONTHLY_CPI": {
        "name": "Consumer Price Index (CPI)",
        "code": "TP.FG.J0",
        "unit": "index",
        "frequency": Frequency.MONTHLY,
        "data_type": DataType.NUMERIC,
        "category": "economy",
        "description": "Monthly inflation rate (CPI)",
    },
    "MONTHLY_PPI": {
        "name": "Producer Price Index (PPI)",
        "code": "TP.FG.UFE",
        "unit": "index",
        "frequency": Frequency.MONTHLY,
        "data_type": DataType.NUMERIC,
        "category": "economy",
        "description": "Monthly producer inflation (PPI)",
    },
    "TEN_YEAR_BOND": {
        "name": "10-Year Government Bond Yield",
        "code": "TP.FMK.GS10Y",
        "unit": "%",
        "frequency": Frequency.DAILY,
        "data_type": DataType.PERCENT,
        "category": "economy",
        "description": "Yield on 10-year Turkish bonds",
    },
}
