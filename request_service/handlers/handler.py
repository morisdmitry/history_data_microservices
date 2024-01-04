import asyncio
import aiohttp
from get_application import get_application
import ssl


async def process_response(symbol, response_json, time_period, suffix_key: str):
    # pass
    app = get_application()
    message = {
        'symbol': symbol,
        'key': suffix_key,
        'period': time_period,
        'value': response_json
    }
    await app.rabbit_mq.publish(message, app.config.rabbitmq_producer_queue_name)



async def fetch(url, params, msg, session: aiohttp.ClientSession, retries=3):
    app = get_application()
    # Disable SSL certificate verification
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    try:
        for i in range(retries):
            try:
                async with session.get(url, params=params, ssl=ssl_context) as response:
                    print(f"response_json status {response.status}")
                    if response.status == 200:
                        response = await response.json()
                        if not response:
                            raise Exception("reponse is NONE once again!!!>>>>>>>>>>>")
                        return response
                    else:
                        response.raise_for_status()
            except aiohttp.ClientError:
                if i == retries - 1:
                    raise
                print(">>> second retry <<<")
                await asyncio.sleep(1)
        raise ValueError("Maximum retries exceeded")
    except Exception as e:
        await asyncio.sleep(2)
        await app.rabbit_mq.publish(msg, app.config.rabbitmq_producer_queue_name)
        print(f">>> ONCE AGAIN <<<<")
        print(f">>> error {e}")


async def process_message(msg):
    api_semaphore = asyncio.Semaphore(10)
    async with api_semaphore:
        get_klines_url = "https://api.binance.com/api/v3/klines"
        start_time, end_time = msg["range"].split(":", 1)
        params = {
            f"symbol": msg["symbol"],
            "startTime": start_time,
            "endTime": end_time,
            "interval": msg["period"],
            "limit": 1000,
        }

        async with aiohttp.ClientSession() as session:
            try:
                response_json = await fetch(
                    get_klines_url,
                    params,
                    msg,
                    session,
                )

                asyncio.create_task(
                    process_response(msg["symbol"], response_json, msg["period"], msg["range"])
                )
            except Exception as e:
                # pass
                print(">>>", e)
