from ..init_imports import *
def require_env(key: str,env_path=None, fallback: str | None = None) -> str:
    val = get_env_value(key=key,path=env_path) or fallback
    if not val:
        raise RuntimeError(f"❌ Missing env var: {key}")
    return val
