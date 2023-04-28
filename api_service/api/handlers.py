from fastapi import APIRouter, Depends

from api.actions import (
    get_only_new_periods,
    get_periods_between,
    period_in_seconds,
    send_message_to_kafka,
)
from api.models import GetStartedPeriods
from services.clients import get_kafka_producer, get_redis
from aiokafka import AIOKafkaProducer
from config import config


hostory_data = APIRouter()


@hostory_data.post("/period_klines")
async def post_message_to_kafka(
    body: GetStartedPeriods,
    producer: AIOKafkaProducer = Depends(get_kafka_producer),
    redis=Depends(get_redis),
):
    """
    range between start and end date min one day
    period in seconds: [
        1s - 1; 1m - 60; 3m - 180; 5m - 300; 5m - 900; 0m - 1800;
        1h - 3600; 2h - 7200; 4h - 14400; 6h - 21600; 8h - 28800;
        2h - 43200; 1d - 86400; 3d - 259200; 1w - 604800; 1M - 2592000;  ]
    """

    time_period = await period_in_seconds(body.period)
    periods = await get_periods_between(body.start_date, body.end_date, time_period)
    print(f"get_periods_between {len(periods)}")
    periods = await get_only_new_periods(redis, body.period, periods)
    if not periods:
        return {"message": f"all data exists in database"}

    for period in periods:
        message = {}
        message["symbol"] = body.symbol
        message["range"] = period
        message["period"] = body.period
        # print(f"message {message}")
        await send_message_to_kafka(producer, config.KAFKA_TOPIC, message)

    return {"message": f"Message '{body}' sent to Kafka topic '{body}'"}
