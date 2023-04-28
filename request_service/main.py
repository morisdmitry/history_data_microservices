import asyncio
import json
import aiohttp
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer


async def fetch_with_retry(url, params, session, retries=3):
    for i in range(retries):
        try:
            async with session.get(url, params=params) as response:
                print(f"response_json status {response.status}")
                if response.status == 200:
                    return await response.json()
                else:
                    response.raise_for_status()
        except aiohttp.ClientError:
            if i == retries - 1:
                raise
            print(">>> second retry <<<")
            await asyncio.sleep(1)
    raise ValueError("Maximum retries exceeded")


async def process_message(message):
    async with api_semaphore:
        # Extract the symbol from the message
        # print("message", message)
        str_data = message.value
        dict_data = json.loads(str_data)
        # print(f"dict_data", dict_data)
        get_klines_url = "https://api.binance.com/api/v3/klines"
        start_time, end_time = dict_data["range"].split(":", 1)
        params = {
            f"symbol": dict_data["symbol"],
            "startTime": start_time,
            "endTime": end_time,
            "interval": dict_data["period"],
            "limit": 1000,
        }

        # print(f"params {params}")
        # Make an asynchronous request to the Binance API
        async with aiohttp.ClientSession() as session:
            # print(f"params {params}")
            try:
                response_json = await fetch_with_retry(get_klines_url, params, session)
                # Process the response asynchronously

                asyncio.create_task(
                    process_response(
                        response_json, dict_data["period"], dict_data["range"]
                    )
                )
            except Exception as e:
                # pass
                print(">>>", e)


async def process_response(response_json, time_period, suffix_key: str):
    # Do something with the response asynchronously
    # print("symbol", response_json)
    print("response_json", len(response_json))
    print("response_json ok", f"{suffix_key}")
    # pass
    producer = AIOKafkaProducer(
        bootstrap_servers="localhost:9092",
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )
    await producer.start()

    try:
        message = {}
        message["key"] = suffix_key
        message["period"] = time_period
        message["value"] = response_json
        await producer.send("topic2", value=message)
    finally:
        await producer.stop()


async def consume_messages():
    consumer = AIOKafkaConsumer(
        "topic1",
        bootstrap_servers="localhost:9092",
        value_deserializer=lambda m: m.decode("utf-8"),
    )

    await consumer.start()

    async for msg in consumer:
        asyncio.create_task(process_message(msg))

    await consumer.stop()


if __name__ == "__main__":
    api_semaphore = asyncio.Semaphore(40)

    asyncio.run(consume_messages())
