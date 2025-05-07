import argparse
import asyncio
import os
import uvicorn
import turtle

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

lock = asyncio.Lock()

app = FastAPI()
router = APIRouter()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

screen = turtle.Screen()
screen.title("Turtle Commander")
t = turtle.Turtle()
t.speed(1)

commands = {
    "pendown": t.pendown,
    "penup": t.penup,
    "move": t.forward,
    "left": t.left,
    "right": t.right
}

@app.get("/command/")
async def command(command: str):
    command = command.lower()

    try:
        parts = command.split()
        action = parts[0]

        if action in ["penup", "pendown"]:
            async with lock:
                commands[action]()
            return

        if len(parts) != 2:
            print("Invalid number of arguments: " + command)
            return

        value = int(parts[1])
        if action in ["move", "left", "right"]:
            async with lock:
                commands[action](value)
            return

        print("Invalid Command: " + command)
    except Exception as e:
        print("ERROR Command: " + str(e))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", default=9005)
    args = parser.parse_args()

    if "TURTLE_BACKEND_TARGET" in os.environ:
        backend_port = int(os.environ["TURTLE_BACKEND_TARGET"].split(":")[-1])
    else:
        backend_port = int(args.port)

    app.include_router(router)
    uvicorn.run(app, host="0.0.0.0", port=backend_port)
