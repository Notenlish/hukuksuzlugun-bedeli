# hukuksuzlugun-bedeli

# todo
- seo, date by date pages for each date idfkg
- more Data
- sektör ileri gelenleri açıklamaları
- better ui
- önemli adaletsizlikler arşivi(veya veritabanına ekle)
- kaç kişi işten çıkarıldı ölç
- grafikler
- embed


for `DATABASE_URL`, it should start with `postgresql://` instead of `postgre://`.
If you use `postgre://` then it will give this error: `sqlalchemy.exc.NoSuchModuleError: Can't load plugin: sqlalchemy.dialects:postgres`

EVDS api wont work with cloudflare warp, nor will it work with a vpn.
generate the `API_ACCESS_KEY` for the backend via: `openssl rand -base64 32`

## Database Commands

Nope I dont use aerich

## ENV Variables
DATABASE_URL = "sqlite://db.sqlite3"
TCMB_EVDS2_API_KEY = [api_key_here]
ENV = "DEV" or "PROD"
API_ACCESS_KEY = [api key to the backend]

db is sqlite3 now, I changed it. Its not postgre anymore

## Statistics bla bla bla
use `prometheus`, with `prometheus-fastapi-instrumentator` or `statsd-exporter`
use `easyscheduler` for scheduled statistics collection
