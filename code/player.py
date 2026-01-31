import pygame
from constants import PLAYER_SPEED, PLAYER_MAX_HP, MAP_WIDTH, BLUE

class Player:
    def __init__(self, x=100, y=400, w=50, h=100):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = BLUE
        self.hp = PLAYER_MAX_HP
        self.heavy_cd = 0

    def update(self):
        keys = pygame.key.get_pressed()
        dx = 0
        if keys[pygame.K_LEFT]:
            dx = -PLAYER_SPEED
        elif keys[pygame.K_RIGHT]:
            dx = PLAYER_SPEED

        self.rect.x += dx
        # clamp horizontal to mapa
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > MAP_WIDTH:
            self.rect.right = MAP_WIDTH

    def draw(self, screen, cam_x):
        r = self.rect.copy()
        r.x += cam_x
        pygame.draw.rect(screen, self.color, r)
