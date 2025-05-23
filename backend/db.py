import os

import dotenv
from tortoise import Tortoise

dotenv.load_dotenv(".env")

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL wasn't set.")


async def init_db():
    await Tortoise.init(db_url=DATABASE_URL, modules={"models": ["models"]})
    if os.getenv("ENV") != "production":  # use aerich(cli) if in prod
        await Tortoise.generate_schemas()


async def close_db():
    await Tortoise.close_connections()
