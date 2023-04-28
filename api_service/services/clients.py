import json

from config import config
from aiokafka import AIOKafkaProducer
import aioredis


async def get_kafka_producer() -> AIOKafkaProducer:
    # Create a Kafka producer instance
    producer = AIOKafkaProducer(
        bootstrap_servers=config.KAFKA_URL,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )
    # Connect to Kafka
    await producer.start()
    return producer


async def get_redis() -> aioredis:
    # Create a redis db instance
    redis = await aioredis.from_url("redis://localhost:6377")
    return redis


