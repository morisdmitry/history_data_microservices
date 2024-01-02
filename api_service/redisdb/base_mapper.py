import __main__
from aioredis import Redis
from get_application import get_application


class BaseMapper:
    def __init__(self, redis: Redis = None):
        if not redis:
            redis = get_application().redis
        self.redis: Redis = redis
        self.store_name = ""
