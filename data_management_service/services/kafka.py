import json
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer


async def get_kafka_consumer(topic, kafka_host) -> AIOKafkaProducer:
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=kafka_host,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    )

    await consumer.start()
    return consumer
