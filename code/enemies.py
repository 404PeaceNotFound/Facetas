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
    def __init__(self, x, hp, damage, is_boss=False, y=400, w=128, h=128):
        self.rect = pygame.Rect(x, y, w, h)
        self.is_boss = is_boss
        self.color = YELLOW if is_boss else RED
        self.max_hp = hp
        self.hp = self.max_hp
        self.damage = damage
        self.alive = True

        # --- SISTEMA DE ANIMAÇÃO ---
        self.frames = []
        self.current_frame = 0
        self.animation_speed = 8  # Velocidade da troca (frames por atualização)
        self.frame_index = 0.0      # Acumulador decimal para controle fino do tempo

        try:
            self.sheet = pygame.image.load("./assets/mascara_do_medo.png").convert_alpha()
            self.load_frames(w, h)
            
            if self.is_boss:
                self.frames = [pygame.transform.scale(f, (int(w * 1.5), int(h * 1.5))) for f in self.frames]
                self.rect.size = (int(w * 1.5), int(h * 1.5))
        except:
            self.sheet = None

    def load_frames(self, w, h):
        sheet_width = self.sheet.get_width()
        num_frames = sheet_width // w
        
        for i in range(num_frames):
            pos_x = i * w
            frame = self.sheet.subsurface(pygame.Rect(pos_x, 0, w, h))
            self.frames.append(frame)

    def update_animation(self):
        if self.frames:
            self.frame_index += self.animation_speed
            if self.frame_index >= len(self.frames):
                self.frame_index = 0
            self.current_frame = int(self.frame_index)

    def draw(self, screen, cam_x):
        if not self.alive:
            return
            
        self.update_animation()
            
        r = self.rect.copy()
        r.x += cam_x

        if self.frames:
            screen.blit(self.frames[self.current_frame], r)
        else:
            pygame.draw.rect(screen, self.color, r)
            
        if self.is_boss:
            pygame.draw.rect(screen, WHITE, r, 3)

    def take_damage(self, amount):
        if not self.alive:
            return
        self.hp -= amount
        if self.hp <= 0:
            self.alive = False