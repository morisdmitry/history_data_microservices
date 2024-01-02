import asyncio
import os

from aiokafka import AIOKafkaConsumer
import aioredis
from aioredis.exceptions import TimeoutError as RedisTimeoutError, RedisError
import json

from services.kafka import get_kafka_consumer
from services.redis import get_redis
from services.mongo import get_mongo


class TimeoutError(asyncio.TimeoutError, RedisError):
    pass


topic = os.environ.get("KAFKA_TOPIC", default="topic2")
redis_url = os.environ.get("REDIS_HOST", default="localhost:6377")
kafka_host = os.environ.get("KAFKA_HOST", default="localhost:9092")

print(f"topic {topic}")
print(f"redis_url {redis_url}")
print(f"kafka_host {kafka_host}")


async def save_to_db(semaphore, redis, mongo, message):
    async with semaphore:
        print(f"save {message['key']}")
        params = {
            "starttime:endtime": message["key"],
            "starttime": int(message["key"].split(":")[0]),
            "endtime": int(message["key"].split(":")[1]),
            "period": message["period"],
            "data": message["value"],
        }
        await mongo.records.insert_one(params)
        await redis.sadd(f'keys:{message["period"]}', f'{message["key"]}')


async def consume_messages(semaphore):
    consumer = await get_kafka_consumer(topic, kafka_host)
    redis = await get_redis()
    mongo = await get_mongo()
    async for msg in consumer:
        asyncio.create_task(save_to_db(semaphore, redis, mongo, msg.value))

    await consumer.stop()


async def main():
    semaphore = asyncio.Semaphore(30)

    await consume_messages(semaphore)


if __name__ == "__main__":
    asyncio.run(main())
