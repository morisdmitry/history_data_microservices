from pydantic import BaseModel
from datetime import date


class GetStartedPeriods(BaseModel):
    symbol: str = "ETHBUSD"
    start_date: date = "2022-01-01"
    end_date: date = "2023-01-01"
    period: str = "1s"
