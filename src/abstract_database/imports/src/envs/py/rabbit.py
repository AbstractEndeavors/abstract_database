# src/env/rabbit.py
from .imports import get_env_value

_RABBIT_DISPLAYED = False





def load_rabbit_env(env_path=None) -> dict:
    global _RABBIT_DISPLAYED

    host = require_env(key="SOLCATCHER_AMQP_HOST", fallback="127.0.0.1",env_path=env_path)
    port = int(require_env(key="SOLCATCHER_AMQP_PORT", fallback="6044",env_path=env_path))
    user = require_env(key="SOLCATCHER_AMQP_USER",fallback="solcatcher",env_path=env_path)
    password = require_env(key="SOLCATCHER_AMQP_PASS",fallback="solcatcher",env_path=env_path)
    vhost = require_env(key="SOLCATCHER_AMQP_VHOST",fallback="solcatcher",env_path=env_path)

    out = {
        "host": host,
        "port": port,
        "user": user,
        "password": password,
        "vhost": vhost,
        "url": f"amqp://{user}:{password}@{host}:{port}/{vhost}",
    }

    if not _RABBIT_DISPLAYED:
        print("🐇 Rabbit config:", out)
        _RABBIT_DISPLAYED = True

    return out
