import dotenv
import os
dotenv.load_dotenv(".env")

TORTOISE_ORM = {
    "connections": {"default": f"{os.environ['DATABASE_URL']}"},
    "apps": {
        "models": {
            # backend.models = curdir içindeki backend klasörü içindeki models dosyasını al
            # bendeki modeller direkten current working directory içerisinde, o yüzden direkten models olacak
            "models": ["models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
