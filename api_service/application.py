import aioredis

from config.config import ConfigModel
from rabbitmq.RabbitMQ import RabbitMQ


class Application:
    def __init__(self):
        self.config: ConfigModel = None
        self.rabbit_mq = None
        self.redis = None
        self.service_name = "history_data_api_service"

    async def init_async(self):
        self.rabbit_mq = RabbitMQ(
            self.config.rabbitmq_login,
            self.config.rabbitmq_password,
            self.config.rabbitmq_host,
            self.config.rabbitmq_port,
            self.config.rabbitmq_queue,
        )
        self.redis = await aioredis.from_url(self.config.redis_url)

    def set_config(self, config):
        self.config = config

    def set_service_name(self, name):
        self.service_name = self.service_name + "@" + name
