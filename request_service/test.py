import asyncio
import ssl
import aiohttp
import aio_pika

RATE_LIMIT = 2  # Maximum number of requests per second
CONCURRENCY_LIMIT = 5  # Maximum number of concurrent requests


async def process_query(query):
    # Make the request to the Binance API
    url = "https://api.binance.com/api/v3/klines"
    params = {
        f"symbol": "ETHBUSD",
        "startTime": 1672509000000,
        "endTime": 1672510000000,
        "interval": "1s",
        "limit": 1000,
    }
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, ssl=ssl_context) as response:
            # Process the response
            if response.status == 200:
                data = await response.json()
                # print(f"data {len(data)}")  # Do something with the data
            else:
                print(f"status code : {response.status}")


async def handle_message(message):
    query = message.body.decode()  # Assuming the message body contains the query
    await process_query(query)
    message.ack()  # Acknowledge the message to remove it from the queue


async def consume_messages():
    host = "localhost"
    port = 5672
    login = "login"
    password = "pass"
    connection = await aio_pika.connect_robust(
        host=host,
        port=port,
        login=login,
        password=password,
    )
    channel = await connection.channel()
    queue = await channel.declare_queue("data_receiver_queue")

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            asyncio.ensure_future(handle_message(message))


# Limit the number of requests per second
async def rate_limit_coroutine(semaphore):
    while True:
        async with semaphore:
            await asyncio.sleep(1 / RATE_LIMIT)


# Limit the number of concurrent requests
async def concurrency_limit_coroutine(semaphore):
    while True:
        async with semaphore:
            await asyncio.sleep(0.1)  # Adjust the delay as needed


async def main():
    semaphore_rate_limit = asyncio.Semaphore(RATE_LIMIT)
    semaphore_concurrency_limit = asyncio.Semaphore(CONCURRENCY_LIMIT)

    await asyncio.gather(
        consume_messages(),
        rate_limit_coroutine(semaphore_rate_limit),
        concurrency_limit_coroutine(semaphore_concurrency_limit),
    )


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
