import pygame
from constants import GREEN, RED, YELLOW, WHITE

class NPC:
    def __init__(self, x, text, y=420, w=40, h=80):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = GREEN
        self.text = text
        self.active = True
        global img_enemy
        img_enemy = pygame.image.load(f'assets/images/sprite_vilao_violencia.png').convert_alpha()
        global enemyCaracterRedimision
        enemyCaracterRedimision = pygame.transform.scale(img_enemy, (200, 200))
        global enemyCaracterflip
        enemyCaracterflip = pygame.transform.flip(enemyCaracterRedimision, True, False)

    def draw(self, screen, cam_x):
        if not self.active:
            return
        r = self.rect.copy()
        r.x += cam_x
        pygame.draw.rect(screen, self.color, r)

class Enemy:
    def __init__(self, x, hp, damage, is_boss=False, y=350, w=60, h=100):
        self.rect = pygame.Rect(x, y, w, h)
        self.is_boss = is_boss
        self.color = YELLOW if is_boss else RED
        self.max_hp = hp
        self.hp = self.max_hp
        self.damage = damage
        self.alive = True

    def draw(self, screen, cam_x):
        if not self.alive:
            return
        r = self.rect.copy()
        r.x += cam_x
        #pygame.draw.rect(screen, self.color, r)
        screen.blit(enemyCaracterflip, r)
        if self.is_boss:
            pygame.draw.rect(screen, WHITE, r, 3)

    def take_damage(self, amount):
        if not self.alive:
            return
        self.hp -= amount
        if self.hp <= 0:
            self.alive = False