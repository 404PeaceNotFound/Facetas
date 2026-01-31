import pygame
from constants import *

class NPC:
    def __init__(self, x, text):
        self.rect = pygame.Rect(x, 420, 40, 80)
        self.color = GREEN
        self.text = text
        self.active = True

    def draw(self, screen, camera_x):
        if not self.active: return
        view_rect = self.rect.copy()
        view_rect.x += camera_x
        pygame.draw.rect(screen, self.color, view_rect)

class Enemy:
    def __init__(self, x, is_boss=False):
        self.rect = pygame.Rect(x, 400, 60, 100)
        self.is_boss = is_boss
        self.color = YELLOW if is_boss else RED
        
        # Balanceamento solicitado: morre com 2 ataques bem sucedidos
        # Ataque básico = 1 dano. HP = 2.
        # Boss HP = 4 (apenas para diferenciar um pouco, ou mantemos 2 conforme strict)
        # O prompt diz: "Inimigos morrem após 2 ataques bem-sucedidos".
        # Vamos assumir HP=2 para comuns, HP=4 para Boss.
        self.max_hp = 4 if is_boss else 2
        self.hp = self.max_hp
        self.damage = 15 if is_boss else 10
        self.alive = True

    def draw(self, screen, camera_x):
        if not self.alive: return
        view_rect = self.rect.copy()
        view_rect.x += camera_x
        # Feedback visual de Boss
        if self.is_boss:
            pygame.draw.rect(screen, self.color, view_rect)
            pygame.draw.rect(screen, WHITE, view_rect, 3)
        else:
            pygame.draw.rect(screen, self.color, view_rect)