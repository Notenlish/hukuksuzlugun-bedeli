# hukuksuzlugun-bedeli

![ss.png](screenshot)

A project dedicated to showcasing the economic impact of the 19 March civil coup to the Turkish Economy.

If the server bugs out and cannot fetch data or respond, just make a commit, the deploy gh action will start the code again.

https://x.com/cnbceofficial/status/1927376135135887761 ekonomi iyi gidiyorrrr
https://x.com/bdalgin/status/1927435429264920909
https://x.com/dunyadanborsa/status/1927402934184071461
https://x.com/cnbceofficial/status/1927256388973015467
https://x.com/ebu_melun/status/1927279291928113369

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

## vps commands idk

`sudo systemctl list-units --type=service` -> lists services
`sudo journalctl -u myapp.service -f` -> shows logs realtime
`sudo journalctl -u myapp.service` -> logs
`sudo journalctl -u myapp.service -b` -> logs of current boot
`sudo journalctl -u myapp.service --since "YYYY-MM-DD HH:MM:SS" --until "YYYY-MM-DD HH:MM:SS"` -> filter by time
`sudo ss -tuln | grep 8000` -> this is supposed to give `tcp    LISTEN     0      128    0.0.0.0:8000       0.0.0.0:*`
`sudo ufw status` -> firewall. Look for a rule regarding port 8000
`ping 8.8.8.8` -> ping google
`ping evds2.tcmb.gov.tr` -> ping evds2 servers
`curl -v https://evds2.tcmb.gov.tr/service/evds/categories/type=json`
