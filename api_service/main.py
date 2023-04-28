from fastapi import APIRouter, FastAPI
import uvicorn
from api.handlers import hostory_data


app = FastAPI(title="set and get history data")

main_api_router = APIRouter()
app.include_router(hostory_data)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


# tests
