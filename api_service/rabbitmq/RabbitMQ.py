import asyncio
import json

import aio_pika
from aio_pika import Message
from aio_pika.abc import AbstractRobustQueue, AbstractRobustExchange


class RabbitMQ:
    def __init__(self, login, password, host, port, queue_name):
        self.connection = None
        self.channel = None
        self.queue: AbstractRobustQueue = None
        self.queue_exchange: AbstractRobustExchange = None
        self.login = login
        self.password = password
        self.host = host
        self.port = port
        self.queue_name = queue_name
        self.callback = None
        self.loop = asyncio.get_running_loop()

    async def init_async(self, exchange=False):
        self.connection = await aio_pika.connect_robust(
            host=self.host,
            port=self.port,
            login=self.login,
            password=self.password,
            loop=self.loop,
        )
        self.channel = await self.connection.channel()

        if not exchange:
            self.queue = await self.channel.declare_queue(name=self.queue_name)
        else:
            pass
            # self.queue_exchange = await self.channel.declare_exchange(name='hive-tasks')

    async def publish(self, message):
        message_body = json.dumps(message).encode("utf-8")
        await self.channel.default_exchange.publish(
            Message(
                message_body,
                content_type="application/json",
            ),
            self.queue_name,
        )

    def set_handler(self, callback):
        self.callback = callback
