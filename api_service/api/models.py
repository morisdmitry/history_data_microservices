from pydantic import BaseModel
from datetime import date


class GetStartedPeriods(BaseModel):
    symbol: str = "ETHBUSD"
    start_date: date = "2023-04-07"
    end_date: date = "2023-04-08"
    period: str = "1s"

