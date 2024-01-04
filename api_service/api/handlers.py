import asyncio
from fastapi import APIRouter

from api.actions import (
    get_only_new_periods,
    get_periods_between,
    period_in_seconds,
)
from api.models import GetStartedPeriods

from get_application import get_application


hostory_data = APIRouter()


@hostory_data.post("/period_klines")
async def post_message(data: GetStartedPeriods):
    time_period = period_in_seconds(data.period)
    periods = get_periods_between(data.start_date, data.end_date, time_period)
    print(f"get_periods_between {len(periods)}")
    app = get_application()
    periods = await get_only_new_periods(app.redis, data.period, periods, data.symbol)
    if not periods:
        return {"message": f"all data exists in database"}

    # # Get all tasks
    # all_tasks = asyncio.all_tasks()

    # # Print task information
    # for task in all_tasks:
    #     print(f"    task {task}")
    #     print(">" * 30)

    for period in periods:
        message = {}
        message["symbol"] = data.symbol
        message["range"] = period
        message["period"] = data.period
        print(f"message {message}")
        await app.rabbit_mq.publish(message)

    return {"message": f"Message '{data}' sent to rmq '{data}'"}
