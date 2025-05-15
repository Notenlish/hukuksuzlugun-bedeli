# hukuksuzlugun-bedeli

for `DATABASE_URL`, it should start with `postgresql://` instead of `postgre://`.
If you use `postgre://` then it will give this error: `sqlalchemy.exc.NoSuchModuleError: Can't load plugin: sqlalchemy.dialects:postgres`

EVDS api wont work with cloudflare warp, nor will it work with a vpn.

## Database Commands

aerich init -t your_project.models
aerich init -t settings.TORTOISE_ORM

aerich init-db # ilk kurulum

aerich migrate && aerich upgrade

```sh
aerich init -t config.TORTOISE_ORM
aerich init-db         # veritabanını ilk kez oluşturur
aerich migrate         # yeni migration oluşturur
aerich upgrade         # migration'ı uygular
```

## ENV Variables
DATABASE_URL = "sqlite://db.sqlite3"
TCMB_EVDS2_API_KEY = [api_key_here]
ENV = "DEV" or "PROD"

db is sqlite3 now, I changed it. Its not postgre anymore
