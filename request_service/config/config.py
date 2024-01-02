import os
import yaml
from pydantic import BaseModel


class ConfigModel(BaseModel):
    rabbitmq_host: str
    rabbitmq_port: int
    rabbitmq_login: str
    rabbitmq_password: str
    rabbitmq_consumer_queue_name: str
    rabbitmq_producer_queue_name: str


def recieve_config(env: str) -> ConfigModel:
    path = os.path.join("config", env + ".yaml")
    if not os.path.exists(path):
        raise Exception(f"The file {path} does not exist.")
    with open(path, "r") as f:
        config_data = yaml.safe_load(f)
    return ConfigModel(**config_data)
