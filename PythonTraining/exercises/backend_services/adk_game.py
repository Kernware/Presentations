import pygame
import threading
import uvicorn
from fastapi import FastAPI, Query
from typing import Dict
import math
import time

# Shared game state
player_commands: Dict[str, str] = {"red": "none", "green": "none", "blue": "none"}

# Lock for thread-safe operations on commands
command_lock = threading.Lock()

# FastAPI setup
app = FastAPI()

@app.post("/command")
def set_command(name: str = Query(...), action: str = Query(...)):
    if name not in player_commands:
        return {"error": f"Unknown player {name}"}
    if action not in ["left", "right", "none"]:
        return {"error": "Invalid action. Use left, right, or none."}
    with command_lock:
        player_commands[name] = action
    return {"status": "ok", "player": name, "action": action}

def run_fastapi():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")

# Player class
class Player:
    def __init__(self, name, color, start_pos, angle):
        self.name = name
        self.color = color
        self.x, self.y = start_pos
        self.angle = angle  # in degrees
        self.speed = 2.5
        self.alive = True
        self.trail = []

    def update_direction(self, command):
        if command == "left":
            self.angle -= 5
        elif command == "right":
            self.angle += 5

    def move(self):
        rad = math.radians(self.angle)
        self.x += self.speed * math.cos(rad)
        self.y += self.speed * math.sin(rad)
        self.trail.append((int(self.x), int(self.y)))

    def get_position(self):
        return int(self.x), int(self.y)

# Game constants
WIDTH, HEIGHT = 800, 600
BG_COLOR = (0, 0, 0)
FPS = 60

# Main game function
def run_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Achtung, die Kurve!")
    clock = pygame.time.Clock()

    players = [
        Player("red", (255, 0, 0), (100, 100), 0),
        Player("green", (0, 255, 0), (700, 100), 180),
        Player("blue", (0, 0, 255), (400, 500), 270),
    ]

    trail_surface = pygame.Surface((WIDTH, HEIGHT))
    trail_surface.fill(BG_COLOR)

    running = True
    while running:
        screen.blit(trail_surface, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        with command_lock:
            commands = dict(player_commands)

        for player in players:
            if not player.alive:
                continue
            player.update_direction(commands[player.name])
            player.move()
            x, y = player.get_position()

            # Collision with walls
            if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
                player.alive = False
                continue

            # Collision with trails
            if trail_surface.get_at((x, y)) != BG_COLOR:
                player.alive = False
                continue

            # Draw on trail surface
            pygame.draw.circle(trail_surface, player.color, (x, y), 2)

        # Draw updated screen
        screen.blit(trail_surface, (0, 0))
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

# Start FastAPI in background thread
api_thread = threading.Thread(target=run_fastapi, daemon=True)
api_thread.start()

# Run game (blocking)
run_game()
