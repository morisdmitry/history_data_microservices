import __main__
from motor.motor_asyncio import AsyncIOMotorClient
from get_application import get_application


class BaseMapper:
    def __init__(self, mongodb: AsyncIOMotorClient = None):
        if not mongodb:
            mongodb = get_application().mongodb
        self.mongodb: AsyncIOMotorClient = mongodb

        self.store_name = ""
