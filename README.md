# hukuksuzlugun-bedeli

for `DATABASE_URL`, it should start with `postgresql://` instead of `postgre://`.
If you use `postgre://` then it will give this error: `sqlalchemy.exc.NoSuchModuleError: Can't load plugin: sqlalchemy.dialects:postgres`

EVDS api wont work with cloudflare warp, nor will it work with a vpn.
