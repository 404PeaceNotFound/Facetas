import pygame
from constants import *

class UI:
    def __init__(self, screen):
        self.screen = screen
        self.font_big = pygame.font.SysFont("Arial", 48)
        self.font_small = pygame.font.SysFont("Arial", 24)

    def draw_text(self, text, size, x, y, color=WHITE, center=False):
        font = self.font_big if size == "big" else self.font_small
        surface = font.render(text, True, color)
        rect = surface.get_rect()
        if center:
            rect.center = (x, y)
        else:
            rect.topleft = (x, y)
        self.screen.blit(surface, rect)

    def draw_menu(self, options, selected_index):
        self.screen.fill(BLACK)
        self.draw_text("PROTOTIPO DE AVENTURA", "big", SCREEN_WIDTH//2, 100, center=True)
        
        for i, option in enumerate(options):
            color = YELLOW if i == selected_index else WHITE
            self.draw_text(option, "small", SCREEN_WIDTH//2, 300 + i * 40, color, center=True)

    def draw_dialog(self, text):
        # Caixa de dialogo
        rect = pygame.Rect(50, 450, 700, 100)
        pygame.draw.rect(self.screen, BLACK, rect)
        pygame.draw.rect(self.screen, WHITE, rect, 2)
        self.draw_text(text, "small", 70, 470)
        self.draw_text("Pressione 'E' para fechar", "small", 500, 520, YELLOW)

    def draw_combat_hud(self, player_hp, enemy_hp, round_num, log_text, action_menu, selected_idx, heavy_cd):
        # Barra superior
        pygame.draw.rect(self.screen, GRAY, (0, 0, SCREEN_WIDTH, 80))
        self.draw_text(f"Player HP: {player_hp}", "small", 20, 20, BLUE)
        self.draw_text(f"Enemy HP: {enemy_hp}", "small", 600, 20, RED)
        self.draw_text(f"Round: {round_num}", "small", SCREEN_WIDTH//2, 20, WHITE, center=True)
        
        # Log de combate
        self.draw_text(log_text, "small", SCREEN_WIDTH//2, 55, YELLOW, center=True)

        # Menu de ações (inferior)
        y_base = 500
        for i, action in enumerate(action_menu):
            color = YELLOW if i == selected_idx else WHITE
            txt = action
            if action == "Ataque Pesado" and heavy_cd > 0:
                txt += f" (CD: {heavy_cd})"
                color = GRAY
            
            self.draw_text(txt, "small", 100 + i * 200, y_base, color)