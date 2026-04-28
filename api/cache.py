import os
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

async def init_cache(key_builder=None):
    redis = aioredis.from_url(REDIS_URL, encoding="utf8", decode_responses=True)

    # Attempt to set maxmemory if possible (optional, might fail on some providers)
    try:
        await redis.config_set("maxmemory", "2gb")
        await redis.config_set("maxmemory-policy", "allkeys-lru")
    except Exception as e:
        print(f"Warning: Could not set Redis maxmemory config: {e}")

    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache", key_builder=key_builder)

async def clear_cache():
    """Clears all cached items."""
    redis = aioredis.from_url(REDIS_URL, encoding="utf8", decode_responses=True)
    await redis.flushdb()
    print("Redis cache cleared.")
