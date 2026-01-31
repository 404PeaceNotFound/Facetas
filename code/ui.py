import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, RED, YELLOW, GRAY, BLUE

class UI:
    def __init__(self, screen):
        self.screen = screen
        self.font_big = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 24)

    def draw_text(self, text, big, x, y, color=WHITE, center=False):
        font = self.font_big if big else self.font_small
        surf = font.render(text, True, color)
        rect = surf.get_rect()
        if center:
            rect.center = (x, y)
        else:
            rect.topleft = (x, y)
        self.screen.blit(surf, rect)

    def draw_menu(self, options, selected_index):
        self.screen.fill(BLACK)
        self.draw_text("Facetas", True, SCREEN_WIDTH // 2, 100, center=True)
        for i, opt in enumerate(options):
            color = YELLOW if i == selected_index else WHITE
            self.draw_text(opt, False, SCREEN_WIDTH // 2, 220 + i * 40, color, center=True)

    def draw_dialog(self, text):
        box = pygame.Rect(50, SCREEN_HEIGHT - 140, SCREEN_WIDTH - 100, 100)
        pygame.draw.rect(self.screen, BLACK, box)
        pygame.draw.rect(self.screen, WHITE, box, 2)
        self.draw_text(text, False, box.x + 12, box.y + 12)
        self.draw_text("Pressione 'E' para fechar", False, box.right - 220, box.y + 56, YELLOW)

    def draw_combat_hud(self, player_hp, enemy_hp, round_num, log_text,
                        action_menu, selected_idx, heavy_cd):
        # topo: barras e round
        pygame.draw.rect(self.screen, GRAY, (0, 0, SCREEN_WIDTH, 80))
        self.draw_text(f"Player HP: {player_hp}", False, 12, 18, BLUE)
        self.draw_text(f"Enemy HP: {enemy_hp}", False, SCREEN_WIDTH - 180, 18, RED)
        self.draw_text(f"Round: {round_num}", False, SCREEN_WIDTH // 2, 18, WHITE, center=True)

        # log
        self.draw_text(log_text, False, SCREEN_WIDTH // 2, 52, YELLOW, center=True)

        # ações (inferior)
        y = SCREEN_HEIGHT - 100
        gap = max(160, SCREEN_WIDTH // max(1, len(action_menu)) - 20)
        for i, act in enumerate(action_menu):
            color = YELLOW if i == selected_idx else WHITE
            label = act
            if act.lower().startswith("ataque pesado") and heavy_cd > 0:
                label += f" (CD:{heavy_cd})"
                color = GRAY
            self.draw_text(label, False, 60 + i * gap, y, color)
