import pygame, sys
from constants import *
from map import GameMap, Camera
from player import Player
from enemies import Enemy, NPC
from combat import CombatSystem
from ui import UI

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.ui = UI(self.screen)

        self.menu_options = ["Start", "Créditos"]
        self.menu_index = 0
        
        # Carregamento das imagens de introdução
        try:
            self.img_intro1 = pygame.image.load('Facetas/code/assets/images/historia1.png').convert_alpha()
            self.img_intro2 = pygame.image.load('Facetas/code/assets/images/historia2.png').convert_alpha()
            self.img_intro1 = pygame.transform.scale(self.img_intro1, (SCREEN_WIDTH, SCREEN_HEIGHT))
            self.img_intro2 = pygame.transform.scale(self.img_intro2, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            print("Erro ao carregar imagens de introdução. Usando superfícies vazias.")
            self.img_intro1 = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.img_intro2 = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.running = True
        self.state = STATE_MENU
        self.victory = False
        
        self.dialog_pages = []
        self.current_page_index = 0
        self.dialogo_ja_apareceu = False
        
        self.reset_world()

    def reset_world(self):
        self.player = Player()
        self.map = GameMap()
        self.camera = Camera()
        self.enemies = [
            Enemy(600, hp=4, damage=1),
            Enemy(1200, hp=6, damage=2), 
            Enemy(1800, hp=10, damage=3, is_boss=True)
        ]
        self.npcs = [
            NPC(300, "Cuidado! Inimigos à frente.\nAs setas selecionam a ação.\nPressione 'Enter' para lutar.")
        ]
        self.combat = None
        self.victory = False

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
                else:
                    self.handle_event(event)

            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

    def handle_event(self, event):
        if self.state == STATE_MENU:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.menu_index = (self.menu_index - 1) % len(self.menu_options)
                elif event.key == pygame.K_DOWN:
                    self.menu_index = (self.menu_index + 1) % len(self.menu_options)
                elif event.key == pygame.K_RETURN:
                    if self.menu_index == 0:
                        self.reset_world()
                        self.state = STATE_INTRO1 
                    else:
                        self.state = STATE_CREDITS

        elif self.state == STATE_INTRO1:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.state = STATE_INTRO2

        elif self.state == STATE_INTRO2:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.state = STATE_EXPLORE

        elif self.state == STATE_DIALOG:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                if self.current_page_index < len(self.dialog_pages) - 1:
                    self.current_page_index += 1
                else:
                    self.state = STATE_EXPLORE
                    self.dialogo_ja_apareceu = True
                    self.dialog_pages = []

        elif self.state == STATE_COMBAT and self.combat:
            self.combat.handle_input(event)

        elif self.state == STATE_GAME_OVER:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.state = STATE_MENU

    def update(self):
        if self.state == STATE_EXPLORE:
            self.player.update()
            self.camera.update_follow(self.player.rect)

            # Colisão NPC
            for npc in self.npcs:
                if npc.active and self.player.rect.colliderect(npc.rect):
                    if not self.dialogo_ja_apareceu:
                        self.state = STATE_DIALOG
                        self.dialog_pages = npc.text.split('\n')
                        self.current_page_index = 0
                    break

            # Colisão Inimigo
            for e in self.enemies:
                if e.alive and self.player.rect.colliderect(e.rect):
                    self.start_combat(e)
                    break

        elif self.state == STATE_COMBAT and self.combat:
            self.combat.update() # Lógica sem precisar da screen aqui
            if self.combat.finished:
                if self.combat.result == "WIN":
                    self.combat.enemy.alive = False
                    if self.combat.enemy.is_boss:
                        self.victory = True
                        self.state = STATE_GAME_OVER
                    else:
                        self.state = STATE_EXPLORE
                else:
                    self.state = STATE_GAME_OVER
                
                self.camera.update_follow(self.player.rect)
                self.combat = None

    def start_combat(self, enemy):
        self.state = STATE_COMBAT
        self.combat = CombatSystem(self.player, enemy)

    def draw(self):
        # 1. Telas que cobrem tudo (Menu e Intro)
        if self.state == STATE_MENU:
            self.ui.draw_menu(self.menu_options, self.menu_index)
            pygame.display.flip()
            return

        if self.state == STATE_INTRO1:
            self.screen.blit(self.img_intro1, (0, 0))
            pygame.display.flip()
            return

        if self.state == STATE_INTRO2:
            self.screen.blit(self.img_intro2, (0, 0))
            pygame.display.flip()
            return

        # 2. LIMPEZA DA TELA
        self.screen.fill(BLACK)

        # 3. CAMADA DE FUNDO E PERSONAGENS
        if self.state == STATE_COMBAT and self.combat:
            # DESENHA FUNDO DA BATALHA
            self.screen.blit(self.combat.bg_image, (0, 0))
            
            # DESENHA PERSONAGENS NA ARENA (Sem offset de câmera)
            self.player.draw(self.screen, 0)
            self.combat.enemy.draw(self.screen, 0)
        else:
            # MUNDO NORMAL (Exploração)
            self.map.draw(self.screen, self.camera.x)
            for npc in self.npcs:
                npc.draw(self.screen, self.camera.x)
            for e in self.enemies:
                e.draw(self.screen, self.camera.x)
            self.player.draw(self.screen, self.camera.x)

        # 4. CAMADA DE UI (Sempre por cima)
        if self.state == STATE_DIALOG:
            current_text = self.dialog_pages[self.current_page_index]
            self.ui.draw_dialog(current_text, self.current_page_index, len(self.dialog_pages))

        if self.state == STATE_COMBAT and self.combat:
            self.ui.draw_combat_hud(
                self.player.hp,
                self.combat.enemy.hp,
                self.combat.round,
                self.combat.log,
                self.combat.actions,
                self.combat.selected,
                self.player.heavy_cd
            )

        if self.state == STATE_GAME_OVER:
            if self.victory:
                self.screen.fill(WHITE)
                self.ui.draw_text("VITÓRIA!", True, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, BLACK, center=True)
            else:
                self.screen.fill(BLACK)
                self.ui.draw_text("GAME OVER", True, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, RED, center=True)
            self.ui.draw_text("Enter p/ Menu", False, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50, center=True)

        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()