import pygame
from constants import PLAYER_SPEED, PLAYER_MAX_HP, MAP_WIDTH, BLUE

class Player:
    def __init__(self, x=100, y=400, w=50, h=100):
        self.rect = pygame.Rect(x, y, w, h)
        self.hp = PLAYER_MAX_HP
        self.heavy_cd = 0
        
        # 1. Carregar imagem parada e redimensionar
        # Usamos self. para que essas variáveis pertençam ao jogador
        img_parado = pygame.image.load('code/assets/images/sprite_homem_parado.png').convert_alpha()
        self.mainCaracterRedimision = pygame.transform.scale(img_parado, (100, 150))
        
        # Definimos self.image como a imagem atual que será desenhada
        self.image = self.mainCaracterRedimision
        
        # 2. Carregar lista de sprites de movimento
        self.sprites_andando = [
            pygame.transform.scale(pygame.image.load(f'code/assets/images/movimentoHomemEsquerda{i}.png').convert_alpha(), (100, 150))
            for i in range(1, 5)
        ]
        
        self.frame_atual = 0
        self.olhando_esquerda = False

    def update(self):
        keys = pygame.key.get_pressed()
        dx = 0
        movendo = False 

        if keys[pygame.K_LEFT]:
            dx = -PLAYER_SPEED
            self.olhando_esquerda = True
            movendo = True
        elif keys[pygame.K_RIGHT]:
            dx = PLAYER_SPEED
            self.olhando_esquerda = False
            movendo = True
        
        self.rect.x += dx
        
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > MAP_WIDTH: self.rect.right = MAP_WIDTH

        # 3. Lógica de Animação
        if movendo:
            self.frame_atual += 0.1 
            if self.frame_atual >= len(self.sprites_andando):
                self.frame_atual = 0
            img_temp = self.sprites_andando[int(self.frame_atual)]
        else:
            img_temp = self.mainCaracterRedimision

        # 4. Lógica de Inverter (Flip) - TROCADA AQUI
        # Agora, se estiver olhando para a ESQUERDA, nós invertemos.
        # Se estiver para a DIREITA (else), usamos a imagem original.
        if self.olhando_esquerda:
            self.image = pygame.transform.flip(img_temp, True, False)
        else:
            self.image = img_temp

    def draw(self, screen, cam_x):
        r = self.rect.copy()
        r.x += cam_x
        # DESENHA A VARIÁVEL self.image (que muda no update)
        screen.blit(self.image, r)