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
FASTAPI_ADMIN = {
    "admin_path": "/admin",
    "title": "My Admin Panel",
    #"logo_url": "https://your-logo.com/logo.png",  # optional
    # "template_folders": ["templates"],  # required if using custom templates
    "db_url": os.getenv("DATABASE_URL", None),
}