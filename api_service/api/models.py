from pydantic import BaseModel
from datetime import date


class GetStartedPeriods(BaseModel):
    symbol: str = "ETHUSDT"
    start_date: date = "2022-01-01"
    end_date: date = "2024-01-01"
    period: str = "4h"
