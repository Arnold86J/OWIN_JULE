import os
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

async def init_cache():
    redis = aioredis.from_url(REDIS_URL, encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

async def clear_cache():
    """Clears all cached items."""
    redis = aioredis.from_url(REDIS_URL, encoding="utf8", decode_responses=True)
    await redis.flushdb()
    print("Redis cache cleared.")
