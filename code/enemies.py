import pygame
from constants import GREEN, RED, YELLOW, WHITE

class NPC:
    def __init__(self, x, text, y=420, w=40, h=80):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = GREEN
        self.text = text
        self.active = True

    def draw(self, screen, cam_x):
        if not self.active:
            return
        r = self.rect.copy()
        r.x += cam_x
        pygame.draw.rect(screen, self.color, r)

class Enemy:
    def __init__(self, x, is_boss=False, y=400, w=60, h=100):
        self.rect = pygame.Rect(x, y, w, h)
        self.is_boss = is_boss
        self.color = YELLOW if is_boss else RED
        self.max_hp = 4 if is_boss else 2
        self.hp = self.max_hp
        self.damage = 15 if is_boss else 10
        self.alive = True

    def draw(self, screen, cam_x):
        if not self.alive:
            return
        r = self.rect.copy()
        r.x += cam_x
        pygame.draw.rect(screen, self.color, r)
        if self.is_boss:
            pygame.draw.rect(screen, WHITE, r, 3)

    def take_damage(self, amount):
        if not self.alive:
            return
        self.hp -= amount
        if self.hp <= 0:
            self.alive = False
