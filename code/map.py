import pygame
from constants import *

class Camera:
    def __init__(self):
        self.offset_x = 0

    def update(self, target_rect):
        # Centraliza o alvo
        x = -target_rect.centerx + SCREEN_WIDTH // 2
        
        # Limita às bordas do mapa
        x = min(0, x)  # Esquerda
        x = max(-(MAP_WIDTH - SCREEN_WIDTH), x) # Direita
        
        self.offset_x = x

    def center_on_arena(self, arena_x):
        # Trava a câmera na arena de combate
        x = -arena_x + SCREEN_WIDTH // 2
        x = min(0, x)
        x = max(-(MAP_WIDTH - SCREEN_WIDTH), x)
        self.offset_x = x

class GameMap:
    def __init__(self):
        self.width = MAP_WIDTH
        self.height = MAP_HEIGHT
        self.floor_y = 500  # Nível do chão

    def draw(self, screen, camera_x):
        # Desenha chão
        pygame.draw.rect(screen, (30, 30, 30), 
                        (0 + camera_x, self.floor_y, self.width, SCREEN_HEIGHT - self.floor_y))
        # Bordas visuais
        pygame.draw.line(screen, WHITE, (0 + camera_x, 0), (0 + camera_x, SCREEN_HEIGHT), 5)
        pygame.draw.line(screen, WHITE, (self.width + camera_x, 0), (self.width + camera_x, SCREEN_HEIGHT), 5)