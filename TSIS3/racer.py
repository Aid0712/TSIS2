import pygame
import random

LANES = [150, 300, 450]

class Player:
    def __init__(self):
        self.lane = 1
        self.x = LANES[self.lane]
        self.y = 500
        self.speed = 5
        self.rect = pygame.Rect(self.x, self.y, 50, 80)

        self.active_powerup = None
        self.timer = 0
        self.shield = False

    def move_left(self):
        if self.lane > 0:
            self.lane -= 1
            self.x = LANES[self.lane]

    def move_right(self):
        if self.lane < 2:
            self.lane += 1
            self.x = LANES[self.lane]

    def update(self):
        self.rect.topleft = (self.x, self.y)


class TrafficCar:
    def __init__(self, lane, speed):
        self.x = LANES[lane]
        self.y = -100
        self.speed = speed
        self.rect = pygame.Rect(self.x, self.y, 50, 80)

    def update(self):
        self.y += self.speed
        self.rect.topleft = (self.x, self.y)


class Obstacle:
    def __init__(self, lane):
        self.x = LANES[lane]
        self.y = -100
        self.rect = pygame.Rect(self.x, self.y, 50, 50)

    def update(self, speed):
        self.y += speed
        self.rect.topleft = (self.x, self.y)


class PowerUp:
    def __init__(self, lane, type):
        self.x = LANES[lane]
        self.y = -100
        self.type = type
        self.rect = pygame.Rect(self.x, self.y, 40, 40)

    def update(self, speed):
        self.y += speed
        self.rect.topleft = (self.x, self.y)


def safe_lane(player_lane):
    lanes = [0, 1, 2]
    if random.random() < 0.7:
        lanes.remove(player_lane)
    return random.choice(lanes)


def apply_powerup(player, p):
    if player.active_powerup:
        return

    player.active_powerup = p

    if p == "nitro":
        player.speed += 3
        player.timer = 180

    elif p == "shield":
        player.shield = True

    elif p == "repair":
        player.active_powerup = None


def update_powerup(player):
    if player.active_powerup == "nitro":
        player.timer -= 1
        if player.timer <= 0:
            player.speed -= 3
            player.active_powerup = None