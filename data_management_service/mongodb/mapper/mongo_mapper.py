from get_application import get_application
from mongodb import base_mapper


class MongoMapper(base_mapper.BaseMapper):
    def __init__(self):
        super().__init__()

    async def insert_one(self, params):
        await self.mongodb.records.insert_one(params)
