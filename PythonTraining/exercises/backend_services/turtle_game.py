import argparse
import os
import uvicorn
import turtle

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

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


@app.get("/command/")
async def command(command: str):
    command = command.lower()

    try:
        parts = command.split()
        action = parts[0]

        if action == "move" and len(parts) == 2:
            distance = int(parts[1])
            t.forward(distance)
        elif action == "left" and len(parts) == 2:
            angle = int(parts[1])
            t.left(angle)
        elif action == "right" and len(parts) == 2:
            angle = int(parts[1])
            t.right(angle)
        elif action == "penup":
            t.penup()
        elif action == "pendown":
            t.pendown()
        else:
            pass # invalid command
    except:
        pass # invalid format


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", default=8002)
    args = parser.parse_args()

    if "TURTLE_BACKEND_TARGET" in os.environ:
        backend_port = int(os.environ["TURTLE_BACKEND_TARGET"].split(":")[-1])
    else:
        backend_port = int(args.port)

    app.include_router(router)
    uvicorn.run(app, host="0.0.0.0", port=backend_port)
