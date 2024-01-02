import asyncio
from config.config import recieve_config


from get_application import get_application


if __name__ == "__main__":
    try:
        application = get_application()

        config = recieve_config("dev")
        application.set_config(config)

        loop = asyncio.get_event_loop()

        loop.run_until_complete(application.init_async())
        loop.run_until_complete(application.rabbit_mq.init_async(loop))
        loop.run_until_complete(application.rabbit_mq.worker())

        loop.run_forever()
    except Exception as e:
        print(e)
