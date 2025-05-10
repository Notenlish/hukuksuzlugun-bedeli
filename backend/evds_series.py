from typing import TypedDict
import enum

class Frequency(str, enum.Enum):
    DAILY = "daily"
    MONTHLY = "monthly"

class DataType(str, enum.Enum):
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
