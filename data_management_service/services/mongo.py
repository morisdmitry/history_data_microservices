from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel


class HistoryData(BaseModel):
    pk: str
    data: str


async def get_mongo():
    MONGO_URL = "localhost:27017"
    MONGO_DB = "application"
    client = AsyncIOMotorClient(MONGO_URL)
    # client[MONGO_DB].records.create_index("pk", unique=True)

    return client[MONGO_DB]
