import pygame
from constants import *

class Player:
    def __init__(self):
        self.rect = pygame.Rect(100, 400, 50, 100) # Retângulo azul
        self.color = BLUE
        self.hp = PLAYER_MAX_HP
        self.vel_x = 0
        self.heavy_cd = 0

    def update(self):
        # Movimento básico
        keys = pygame.key.get_pressed()
        self.vel_x = 0
        if keys[pygame.K_LEFT]:
            self.vel_x = -PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.vel_x = PLAYER_SPEED
        
        # Aplica movimento e colisão com bordas
        self.rect.x += self.vel_x
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > MAP_WIDTH: self.rect.right = MAP_WIDTH

    def draw(self, screen, camera_x):
        # Ajusta posição baseado na câmera
        view_rect = self.rect.copy()
        view_rect.x += camera_x
        pygame.draw.rect(screen, self.color, view_rect)