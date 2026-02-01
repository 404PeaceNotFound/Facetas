import pygame
from constants import SCREEN_WIDTH, MAP_WIDTH, MAP_HEIGHT, WHITE

class Camera:
    def __init__(self):
        self.x = 0  # offset horizontal (negativo para mover mundo)

    def update_follow(self, target_rect):
        # centraliza no alvo e limita às bordas do mapa
        x = -target_rect.centerx + SCREEN_WIDTH // 2
        x = min(0, x)
        x = max(-(MAP_WIDTH - SCREEN_WIDTH), x)
        self.x = x

    def center_on(self, world_x):
        # centraliza em uma posição do mundo (ex: arena)
        x = -world_x + SCREEN_WIDTH // 2
        x = min(0, x)
        x = max(-(MAP_WIDTH - SCREEN_WIDTH), x)
        self.x = x

class GameMap:
    def __init__(self):
        self.width = MAP_WIDTH
        self.height = MAP_HEIGHT
        self.floor_y = 500

        try:
            self.bg_image = pygame.image.load('code/assets/images/cenario2.png').convert_alpha()
            # Opcional: Redimensionar para a altura da tela mantendo a proporção ou forçando
            # Aqui forçamos a largura do mapa (2000) e altura da tela (600)
            self.bg_image = pygame.transform.scale(self.bg_image, (self.width, self.height))
        except:
            print("Erro ao carregar assets/cenario2.png. Usando fundo sólido.")
            self.bg_image = None

    def draw(self, screen, cam_x):
        if self.bg_image:
            # Desenhamos o fundo aplicando o deslocamento da câmera
            screen.blit(self.bg_image, (cam_x, 0))
        else:
            # Fundo padrão caso a imagem falhe
            screen.fill((50, 50, 70))
        pygame.draw.rect(screen, (30, 30, 30),
                         (cam_x, self.floor_y, self.width, self.height - self.floor_y))
        # bordas visuais
        pygame.draw.line(screen, WHITE, (cam_x, 0), (cam_x, self.height), 5)
        pygame.draw.line(screen, WHITE, (self.width + cam_x, 0),
                         (self.width + cam_x, self.height), 5)
