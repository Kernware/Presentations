import pygame
import threading
import uvicorn

from fastapi import FastAPI
import math
import time


player_commands = {
    "red": "none",
    "green": "none",
    "blue": "none"
}
command_lock = threading.Lock()

app = FastAPI()


@app.get("/command")
def set_command(name: str, action: str):
    print(f"command, name: {name}, action: {action}")

    if name not in player_commands:
        return {"error": f"Unknown player {name}"}
    if action not in ["left", "right", "none"]:
        return {"error": "Invalid action. Use left, right, or none."}
    with command_lock:
        player_commands[name] = action
    return {"status": "ok", "player": name, "action": action}

def run_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=9003, log_level="warning")

class Player:
    def __init__(self, name, color, start_pos, angle):
        self.name = name
        self.color = color
        self.x, self.y = start_pos
        self.angle = angle  # in degrees
        self.speed = 3.5
        self.alive = True
        self.trail = []

    def update_direction(self, command):
        if command == "left":
            self.angle -= 5
        elif command == "right":
            self.angle += 5

    def move(self):
        rad = math.radians(self.angle)

        old_x = self.x
        old_y = self.y
        self.x += self.speed * math.cos(rad)
        self.y += self.speed * math.sin(rad)
        # print(f"Player Pos: {self.name}, {old_x}/{old_y} -> {self.x}/{self.y}")

        self.trail.append((int(self.x), int(self.y)))

    def get_position(self):
        return int(self.x), int(self.y)

# Game constants
WIDTH, HEIGHT = 800, 600
BG_COLOR = (0, 0, 0)
FPS = 30

def run_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Achtung, die Kurve!")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 72)

    players = [
        Player("red", (255, 0, 0), (100, 110), 0),
        Player("green", (0, 255, 0), (700, 100), 180),
        Player("blue", (0, 0, 255), (400, 500), 270),
    ]

    trail_surface = pygame.Surface((WIDTH, HEIGHT))
    trail_surface.fill(BG_COLOR)

    for count in range(5, 0, -1):
        screen.fill(BG_COLOR)
        text = font.render(str(count), True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        time.sleep(1)

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

            if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
                print(f"Player {player.name}, collided with walls!")
                player.alive = False
                continue

            if trail_surface.get_at((x, y)) != BG_COLOR:
                print(f"Player {player.name}, collided with trail! ({x}, {y})")
                player.alive = False
                continue

            pygame.draw.circle(trail_surface, player.color, (x, y), 2)

        screen.blit(trail_surface, (0, 0))
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

api_thread = threading.Thread(target=run_fastapi, daemon=True)
api_thread.start()

run_game()
