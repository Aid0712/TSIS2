import pygame
import random
import time

from ui import Button
from persistence import *

pygame.init()

# ---------------- SCREEN ----------------
WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

# ---------------- LOAD ----------------
def load_img(path, size):
    try:
        img = pygame.image.load(path)
        return pygame.transform.scale(img, size)
    except:
        surf = pygame.Surface(size)
        surf.fill((200, 200, 200))
        return surf

player_img = load_img("assets/player.png", (50, 80))
enemy_img = load_img("assets/enemy.png", (50, 80))
road_img = load_img("assets/road.png", (600, 700))
nitro_img = load_img("assets/nitro.png", (40, 40))
shield_img = load_img("assets/shield.png", (60, 60))

# ---------------- DATA ----------------
settings = load_settings()
leaderboard = load_leaderboard()

state = "menu"
distance = 0

# ---------------- LANES ----------------
LANES = [80, 160, 240, 320, 400]


def draw_text(text, x, y):
    screen.blit(font.render(text, True, (255, 255, 255)), (x, y))


def safe_lane(player_lane):
    lanes = LANES.copy()
    if player_lane in lanes:
        lanes.remove(player_lane)
    return random.choice(lanes)


# ---------------- PLAYER ----------------
class Player:
    def __init__(self):
        self.lane = 2
        self.x = LANES[self.lane]
        self.y = 550
        self.rect = pygame.Rect(self.x, self.y, 50, 80)

        self.power = None

        # 🛡️ shield
        self.shield_hp = 0

        # ⚡ nitro timer
        self.nitro_start = None

    def move_left(self):
        if self.lane > 0:
            self.lane -= 1
        self.x = LANES[self.lane]

    def move_right(self):
        if self.lane < 4:
            self.lane += 1
        self.x = LANES[self.lane]

    def update(self):
        self.rect.topleft = (self.x, self.y)


# ---------------- ENEMY ----------------
class Car:
    def __init__(self, x, speed):
        self.x = x
        self.y = -100
        self.speed = speed
        self.rect = pygame.Rect(self.x, self.y, 50, 80)

    def update(self):
        self.y += self.speed
        self.rect.topleft = (self.x, self.y)


# ---------------- POWERUP ----------------
class PowerUp:
    def __init__(self, x, t):
        self.x = x
        self.y = -50
        self.type = t
        self.rect = pygame.Rect(self.x, self.y, 40, 40)

    def update(self, speed):
        self.y += speed
        self.rect.topleft = (self.x, self.y)


# ---------------- POWER LOGIC ----------------
def apply_power(player, t):
    if t == "nitro":
        player.power = "nitro"
        player.nitro_start = time.time()   # ⏱️ start 4 sec timer

    elif t == "shield":
        player.shield_hp = 1


# ---------------- NAME INPUT ----------------
def name_input():
    name = ""

    while True:
        screen.fill((0, 0, 0))
        draw_text("Enter name:", 200, 250)
        draw_text(name, 200, 300)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN and name:
                    return name
                elif e.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 10:
                        name += e.unicode

        pygame.display.update()
        clock.tick(60)


# ---------------- MENU ----------------
def menu():
    play = Button("Play", 200, 200, 200, 50)
    lb = Button("Leaderboard", 200, 300, 200, 50)
    st = Button("Settings", 200, 400, 200, 50)

    while True:
        screen.fill((0, 0, 0))

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()

            if e.type == pygame.MOUSEBUTTONDOWN:
                if play.clicked(e.pos):
                    return "game"
                if lb.clicked(e.pos):
                    return "leaderboard"
                if st.clicked(e.pos):
                    return "settings"

        play.draw(screen, font)
        lb.draw(screen, font)
        st.draw(screen, font)

        pygame.display.update()


# ---------------- GAME ----------------
def game():
    global distance

    player = Player()
    cars = []
    powers = []

    distance = 0
    timer = 0
    road_y = 0

    while True:
        screen.fill((30, 30, 30))
        distance += 1

        # EVENTS
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT:
                    player.move_left()
                if e.key == pygame.K_RIGHT:
                    player.move_right()

        # SPEED
        speed = 5 + distance // 500

        # ⚡ NITRO (4 sec auto stop)
        if player.power == "nitro":
            speed += 3

            if player.nitro_start and time.time() - player.nitro_start > 4:
                player.power = None
                player.nitro_start = None

        # ROAD
        road_y += speed
        if road_y >= HEIGHT:
            road_y = 0

        screen.blit(road_img, (0, road_y))
        screen.blit(road_img, (0, road_y - HEIGHT))

        # SPAWN CARS
        timer += 1
        if timer > 50:
            cars.append(Car(safe_lane(player.lane), speed))
            timer = 0

        # SPAWN POWERUPS
        if random.random() < 0.02:
            powers.append(PowerUp(
                safe_lane(player.lane),
                random.choice(["nitro", "shield"])
            ))

        player.update()

        # ---------------- CARS ----------------
        for c in cars[:]:
            c.update()
            screen.blit(enemy_img, (c.x, c.y))

            if player.rect.colliderect(c.rect):

                # 🛡️ SHIELD FIX
                if player.shield_hp > 0:
                    player.shield_hp -= 1
                    cars.remove(c)
                else:
                    return "game_over"

        # ---------------- POWERUPS ----------------
        for p in powers[:]:
            p.update(speed)

            if p.type == "nitro":
                screen.blit(nitro_img, (p.x, p.y))
            else:
                screen.blit(shield_img, (p.x, p.y))

            if player.rect.colliderect(p.rect):
                apply_power(player, p.type)
                powers.remove(p)

        # PLAYER
        screen.blit(player_img, (player.x, player.y))

        # 🛡️ BLUE SHIELD CIRCLE
        if player.shield_hp > 0:
            pygame.draw.circle(
                screen,
                (0, 180, 255),
                (player.x + 25, player.y + 40),
                55,
                3
            )

        draw_text(f"Distance: {distance}", 10, 10)
        draw_text(f"Power: {player.power}", 10, 40)

        pygame.display.update()
        clock.tick(60)


# ---------------- LEADERBOARD ----------------
def leaderboard_screen():
    while True:
        screen.fill((0, 0, 0))

        y = 100
        for i, e in enumerate(leaderboard[:10]):
            draw_text(f"{i+1}. {e['name']} {e['score']}", 150, y)
            y += 30

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()
            if e.type == pygame.KEYDOWN:
                return "menu"

        pygame.display.update()


# ---------------- SETTINGS ----------------
def settings_screen():
    global settings

    while True:
        screen.fill((0, 0, 0))

        draw_text(f"Sound: {settings['sound']}", 150, 200)
        draw_text(f"Difficulty: {settings['difficulty']}", 150, 250)

        draw_text("Press any key", 150, 350)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()
            if e.type == pygame.KEYDOWN:
                save_settings(settings)
                return "menu"

        pygame.display.update()


# ---------------- GAME OVER ----------------
def game_over():
    global leaderboard, distance

    name = name_input()
    score = distance // 5

    leaderboard.append({"name": name, "score": score})
    save_leaderboard(leaderboard)

    return "menu"


# ---------------- MAIN LOOP ----------------
state = "menu"

while True:
    if state == "menu":
        state = menu()
    elif state == "game":
        state = game()
    elif state == "leaderboard":
        state = leaderboard_screen()
    elif state == "settings":
        state = settings_screen()
    elif state == "game_over":
        state = game_over()