# app/utils/cache.py
import json, functools
from redis import Redis
from typing import Callable

# adjust URL if needed
redis_client = Redis.from_url("redis://localhost:6379/0", decode_responses=True)

def make_key(prefix: str, *args, **kwargs) -> str:
    key = prefix + ":" + ":".join(map(str, args))
    if kwargs:
        key += ":" + ":".join(f"{k}={v}" for k, v in sorted(kwargs.items()))
    return key

def cache_response(ttl: int = 60, prefix: str = "cache"):
    """Decorator for synchronous functions that return JSON-serializable dicts."""
    def deco(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = make_key(prefix, func.__name__, *args, **kwargs)
            raw = redis_client.get(key)
            if raw:
                return json.loads(raw)
            result = func(*args, **kwargs)
            try:
                redis_client.setex(key, ttl, json.dumps(result))
            except Exception:
                pass
            return result
        return wrapper
    return deco
