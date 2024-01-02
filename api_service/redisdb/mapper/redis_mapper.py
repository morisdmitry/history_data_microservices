import time
from get_application import get_application
from redisdb import base_mapper


class RedisMapper(base_mapper.BaseMapper):
    def __init__(self):
        super().__init__()
        config = get_application().config
        self.period_in_sec = config.periods_in_sec.dict()

    async def add(self, period, key, limit_cost):
        period_in_sec = self.period_in_sec[period]

        await self.redis.zadd(key, {f"{time.time()}:{limit_cost}": time.time()})

        # create expire if its doesnt exist for current key
        await self.add_expire(key, int(period_in_sec))

    async def check_quantity(self, period, key):
        period_in_sec = self.period_in_sec[period]

        result = await self.redis.zrangebyscore(
            key, int(time.time() - period_in_sec), time.time()
        )
        last_integers = list(map(lambda x: int(x.split(b":")[-1]), result))
        return last_integers

    async def ttl(self, key) -> int:
        return int(await self.redis.ttl(key))

    async def add_expire(self, key, period_in_sec: int):
        await self.redis.expire(key, period_in_sec)

    async def is_flag(self, key, postfix):
        return await self.redis.get(f"{key}:{postfix}")

    async def setnx_flag(self, key, period, postfix, value="Default"):
        await self.redis.setnx(f"{key}:{postfix}", value)

        if await self.ttl(f"{key}:{postfix}") < 0:
            await self.add_expire(f"{key}:{postfix}", self.period_in_sec[period])

    async def set_flag(self, key, period, postfix, value="Default"):
        await self.redis.set(f"{key}:{postfix}", value)

        if await self.ttl(f"{key}:{postfix}") < 0:
            await self.add_expire(f"{key}:{postfix}", self.period_in_sec[period])

    async def remove_flag(self, key, postfix):
        return await self.redis.delete(f"{key}:{postfix}")
