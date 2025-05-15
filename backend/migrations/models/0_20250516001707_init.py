from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "trackedmetric" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" VARCHAR(255) NOT NULL UNIQUE,
    "description" TEXT,
    "category" VARCHAR(255),
    "source" VARCHAR(255),
    "evds_code" VARCHAR(255),
    "url" VARCHAR(255),
    "unit" VARCHAR(255),
    "data_type" VARCHAR(7) NOT NULL DEFAULT 'numeric' /* numeric: numeric\nboolean: boolean\ntext: text\npercent: percent */,
    "frequency" VARCHAR(13) NOT NULL DEFAULT 'daily' /* DAILY: daily\nWORKDAY: workday\nWEEKLY: weekly\nTWICE_A_MONTH: twice_a_month\nMONTHLY: monthly\nQUARTERLY: quarterly\nSIX_MONTHS: six_months\nYEARLY: yearly */
);
CREATE TABLE IF NOT EXISTS "metricdatapoint" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "date" DATE NOT NULL,
    "value" REAL,
    "value_text" TEXT,
    "metric_id" INT NOT NULL REFERENCES "trackedmetric" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_metricdatap_metric__808052" UNIQUE ("metric_id", "date")
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
