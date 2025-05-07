import argparse
import os
import random
import uvicorn

from fastapi import APIRouter, FastAPI, status
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException
from pathlib import Path

app = FastAPI()
router = APIRouter()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/v1/sensor/")
async def v1_sensor():
    return 22


# NOTE: not concurrency safe
SENSOR_V2_TEMP: int = 25

@app.get("/v2/sensor/")
async def v2_sensor():
    global SENSOR_V2_TEMP
    SENSOR_V2_TEMP += random.randint(-1, 1)
    SENSOR_V2_TEMP = min(max(SENSOR_V2_TEMP, -5), 40)
    return SENSOR_V2_TEMP


# NOTE: not concurrency safe
SENSOR_V3_TEMP: int = 25

@app.get("/v3/sensor/")
async def v3_sensor():
    global SENSOR_V3_TEMP
    SENSOR_V3_TEMP += random.randint(-1, 1)
    SENSOR_V3_TEMP = min(max(SENSOR_V3_TEMP, -5), 40)
    return {
        "temperature": SENSOR_V3_TEMP,
        "error": "none"
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="FastAPI backend for mobile teststation."
    )
    parser.add_argument("-p", "--port", default=9004)
    args = parser.parse_args()

    if "BACKEND_TARGET" in os.environ:
        backend_port = int(os.environ["BACKEND_TARGET"].split(":")[-1])
    else:
        backend_port = int(args.port)

    app.include_router(router)
    uvicorn.run(app, host="0.0.0.0", port=backend_port)
