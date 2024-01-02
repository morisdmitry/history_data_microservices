import asyncio
import json

import aio_pika
from aio_pika import Message
from aio_pika.abc import AbstractRobustQueue, AbstractRobustExchange
import traceback


class RabbitMQ:
    def __init__(self, login, password, host, port, consumer_queue_name):
        self.connection = None
        self.channel = None
        self.consumer_queue: AbstractRobustQueue = None
        self.queue_exchange: AbstractRobustExchange = None
        self.login = login
        self.password = password
        self.host = host
        self.port = port
        self.consumer_queue_name = consumer_queue_name
        self.callback = None
        self.loop = None

    async def init_async(self, loop, exchange=False):
        self.loop = loop
        self.connection = await aio_pika.connect_robust(
            host=self.host,
            port=self.port,
            login=self.login,
            password=self.password,
            loop=self.loop,
        )
        self.channel = await self.connection.channel()

        if not exchange:
            self.consumer_queue = await self.channel.declare_queue(
                name=self.consumer_queue_name
            )

        else:
            pass
            # self.queue_exchange = await self.channel.declare_exchange(name='hive-tasks')

    async def publish(self, message: dict, queue_name):
        message_body = json.dumps(message).encode("utf-8")
        await self.channel.default_exchange.publish(
            Message(
                message_body,
                content_type="application/json",
            ),
            queue_name,
        )

    def set_handler(self, callback):
        self.callback = callback

    async def worker(self):
        print("Worker listener run")
        async with self.consumer_queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    if self.callback:
                        try:
                            msg = json.loads(message.body.decode())

                            asyncio.create_task(self.callback(msg))
                        except:
                            print("Catch Task Error")
                            print(traceback.format_exc())
                            continue

        await self.connection.close()
