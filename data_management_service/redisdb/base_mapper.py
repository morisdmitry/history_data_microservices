import __main__
from aioredis import Redis
from get_application import get_application


class BaseMapper:
    def __init__(self, redis: Redis = None):
        if not redis:
            redisdb = get_application().redisdb
        self.redisdb: Redis = redisdb
        self.store_name = ""
