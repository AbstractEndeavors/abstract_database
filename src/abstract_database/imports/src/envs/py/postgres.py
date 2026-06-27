# src/env/postgres.py
from .imports import *

_POSTGRES_DISPLAYED = False


def load_postgres_env(env_path=None) -> dict:
    global _POSTGRES_DISPLAYED

    host = require_env(key="SOLCATCHER_POSTGRESQL_HOST",fallback='127.0.0.1',env_path=env_path)
    port = int(require_env(key="SOLCATCHER_POSTGRESQL_PORT",fallback='1234',env_path=env_path))
    user = require_env(key="SOLCATCHER_POSTGRESQL_USER",fallback='solcatcher',env_path=env_path)
    password = require_env(key="SOLCATCHER_POSTGRESQL_PASS",fallback='solcatcher',env_path=env_path)
    
    database = require_env(key="SOLCATCHER_POSTGRESQL_NAME",fallback='solcatcher1',env_path=env_path)

    out = {
        "host": host,
        "port": port,
        "user": user,
        "password": password,
        "database": database,
        "url": f"postgresql://{user}:{password}@{host}:{port}/{database}",
    }

    if not _POSTGRES_DISPLAYED:
        print("📦 postgres config:", out)
        _POSTGRES_DISPLAYED = True

    return out
