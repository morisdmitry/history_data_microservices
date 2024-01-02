import asyncio


from config.config import ConfigModel
from rabbitmq.RabbitMQ import RabbitMQ
from handlers.handler import process_message


class Application:
    def __init__(self):
        self.config: ConfigModel = None

        self.service_name = "main-hive"

    async def init_async(self):
        self.rabbit_mq = RabbitMQ(
            self.config.rabbitmq_login,
            self.config.rabbitmq_password,
            self.config.rabbitmq_host,
            self.config.rabbitmq_port,
            self.config.rabbitmq_consumer_queue_name,
        )
        self.rabbit_mq.set_handler(process_message)

    def set_config(self, config):
        self.config = config

    def set_service_name(self, name):
        self.service_name = self.service_name + "@" + name

    def init_main_workers(self):
        asyncio.ensure_future(self.run_periodically(3600, self.cleaner))

    async def run_periodically(self, wait_time, func, *args):
        """
        Helper for schedule_task_periodically.
        Wraps a function in a coroutine that will run the
        given function indefinitely
        :param wait_time: seconds to wait between iterations of func
        :param func: the function that will be run
        :param args: any args that need to be provided to func
        """
        while True:
            await func(*args)
            await asyncio.sleep(wait_time)
