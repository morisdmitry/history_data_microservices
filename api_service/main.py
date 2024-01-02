import asyncio
from fastapi import FastAPI
import uvicorn

from config.config import recieve_config
from get_application import get_application
from api.handlers import hostory_data


# tests


app = FastAPI(title="set and get history data")
app.include_router(hostory_data)


@app.on_event("startup")
async def startup_event():
    config = recieve_config("dev")

    application = get_application()
    application.set_config(config)
    application.set_service_name("history_data_api_service")
    await application.init_async()
    await application.rabbit_mq.init_async()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        uvicorn.run("main:app", host="0.0.0.0", port=8700, reload=True)
    )
