import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, RED, YELLOW, GRAY, BLUE, GREEN

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
        self.background_image = pygame.image.load("./Facetas/code/assets/images/menu_background.jpg")
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(self.background_image, (0, 0))
        self.draw_text("Facetas", 100, SCREEN_WIDTH // 2, 100, center=True)
        for i, opt in enumerate(options):
            color = YELLOW if i == selected_index else WHITE
            self.draw_text(opt, False, SCREEN_WIDTH // 2, 220 + i * 40, color, center=True)

    def draw_dialog(self, text, current_page, total_pages):
        box = pygame.Rect(50, SCREEN_HEIGHT - 140, SCREEN_WIDTH - 100, 100)
        pygame.draw.rect(self.screen, BLACK, box)
        pygame.draw.rect(self.screen, WHITE, box, 2)
        
        # Desenha o texto da página atual
        self.draw_text(text, False, box.x + 20, box.y + 20)
        
        # Indicador de página e botão pular
        indicator = f"{current_page + 1}/{total_pages}"
        self.draw_text(indicator, False, box.right - 40, box.bottom - 30, GRAY, center=True)
        self.draw_text("'E' Próximo", False, box.right - 100, box.y + 60, YELLOW)

    def draw_combat_hud(self, player_hp, enemy_hp, round_num, log_text,
                        action_menu, selected_idx, heavy_cd):
        # Topo
        pygame.draw.rect(self.screen, GRAY, (0, 0, SCREEN_WIDTH, 80))
        self.draw_text(f"Player HP: {player_hp}", False, 20, 18, GREEN)
        self.draw_text(f"Enemy HP: {enemy_hp}", False, SCREEN_WIDTH - 120, 18, RED)
        self.draw_text(f"Round: {round_num}", False, SCREEN_WIDTH // 2, 18, WHITE, center=True)

        # Log
        self.draw_text(log_text, False, SCREEN_WIDTH // 2, 52, YELLOW, center=True)

        # Ações (Inferior) - Lógica de centralização corrigida
        y = SCREEN_HEIGHT - 60
        num_actions = len(action_menu)
        # Divide a tela em seções iguais para cada botão
        section_width = SCREEN_WIDTH // num_actions
        
        for i, act in enumerate(action_menu):
            color = YELLOW if i == selected_idx else WHITE
            label = act
            if act.lower().startswith("ataque pesado") and heavy_cd > 0:
                label += f" (CD:{heavy_cd})"
                color = GRAY
            
            # O X é o centro da seção correspondente
            center_x = (i * section_width) + (section_width // 2)
            self.draw_text(label, False, center_x, y, color, center=True)
