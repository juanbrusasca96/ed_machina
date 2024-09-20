import json
import os
from redis import Redis


redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = os.getenv("REDIS_PORT", 6379)

redis_client = Redis(host=redis_host, port=redis_port, db=0)


def get_cache(key: str):
    data = redis_client.get(key)
    if data:
        return json.loads(data)
    return None


def set_cache(key: str, value: dict, ttl: int = 60):
    redis_client.setex(key, ttl, json.dumps(value))
