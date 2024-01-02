import aioredis


async def get_redis():
    redis = await aioredis.from_url("redis://localhost:6377")
    return redis
