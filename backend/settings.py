import dotenv
import os
dotenv.load_dotenv(".env")

TORTOISE_ORM = {
    "connections": {"default": f"{os.environ['DATABASE_URL']}"},
    "apps": {
        "models": {
            "models": ["backend.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
