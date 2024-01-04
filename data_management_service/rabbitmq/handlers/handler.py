import asyncio
from mongodb.mapper.mongo_mapper import MongoMapper
from redisdb.mapper.redis_mapper import RedisMapper


async def process_message(message):
    async with asyncio.Semaphore(30):
        print(f"save {message['key']}")
        print(f"save {message['symbol']}")
        params = {
            "starttime:endtime": message["key"],
            "starttime": int(message["key"].split(":")[0]),
            "endtime": int(message["key"].split(":")[1]),
            "period": message["period"],
            "symbol": message["symbol"],
            "data": message["value"],
        }
        await MongoMapper().insert_one(params)
        await RedisMapper().add(message)
