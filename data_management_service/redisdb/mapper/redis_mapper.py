from redisdb import base_mapper


class RedisMapper(base_mapper.BaseMapper):
    def __init__(self):
        super().__init__()

    async def add(self, message):
        await self.redisdb.sadd(f'keys:{message["symbol"]}:{message["period"]}', f'{message["key"]}')
