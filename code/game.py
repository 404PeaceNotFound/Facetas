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

        self.running = True
        self.state = STATE_MENU
        self.victory = False
        
        # Variáveis para controle de diálogo
        self.dialog_pages = []
        self.current_page_index = 0
        
        self.reset_world()

    def reset_world(self):
        self.player = Player()
        self.map = GameMap()
        self.camera = Camera()
        self.enemies = [
            Enemy(600, hp=4, damage=4),
            Enemy(1200, hp=6, damage=6), 
            Enemy(1800, hp=10, damage=10, is_boss=True)
        ]
        # NPC com texto quebrado por \n
        self.npcs = [
            NPC(300, "Cuidado! Inimigos à frente.\nAs setas selecionam a ação.\nPressione 'Enter' para usar a ação.")
        ]
        self.combat = None
        self.dialogo_ja_apareceu = False
        self.victory = False

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
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
                        self.state = STATE_EXPLORE
                    else:
                        self.state = STATE_CREDITS

        elif self.state == STATE_CREDITS:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.state = STATE_MENU

        elif self.state == STATE_DIALOG:
            # Avança o texto ao pressionar E
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                # Verifica se ainda tem páginas
                if self.current_page_index < len(self.dialog_pages) - 1:
                    self.current_page_index += 1
                else:
                    # Fim do diálogo
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

            # Colisão NPC -> Dialogo
            for npc in self.npcs:
                if npc.active and self.player.rect.colliderect(npc.rect):
                    if not self.dialogo_ja_apareceu:
                        self.state = STATE_DIALOG
                        # Divide o texto do NPC pelo caractere \n
                        raw_text = npc.text
                        self.dialog_pages = raw_text.split('\n')
                        self.current_page_index = 0
                    break

            # Colisão Inimigo -> Combate
            for e in self.enemies:
                if e.alive and self.player.rect.colliderect(e.rect):
                    self.start_combat(e)
                    break

        elif self.state == STATE_COMBAT and self.combat:
            self.combat.update()
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
                
                # Reseta câmera para seguir o player após combate
                self.camera.update_follow(self.player.rect)
                self.combat = None

    def start_combat(self, enemy):
        # Centraliza a câmera na posição original do inimigo (centro da arena)
        self.camera.center_on(enemy.rect.centerx)
        self.state = STATE_COMBAT
        
        # O construtor do CombatSystem agora posiciona os bonecos
        self.combat = CombatSystem(self.player, enemy)

    def draw(self):
        if self.state == STATE_MENU:
            self.ui.draw_menu(self.menu_options, self.menu_index)
            pygame.display.flip()
            return

        if self.state == STATE_CREDITS:
            self.screen.fill(BLACK)
            self.ui.draw_text("Créditos", True, 50, 50)
            self.ui.draw_text("Dev: User", False, 50, 150)
            self.ui.draw_text("Pressione ENTER para Sair", False, 50, 500, RED)
            pygame.display.flip()
            return

        # Desenho do Mundo
        self.screen.fill(BLACK)
        self.map.draw(self.screen, self.camera.x)

        for npc in self.npcs:
            npc.draw(self.screen, self.camera.x)
        for e in self.enemies:
            e.draw(self.screen, self.camera.x)
        self.player.draw(self.screen, self.camera.x)

        if self.state == STATE_DIALOG:
            # Passamos o texto atual e contagem de páginas para UI
            current_text = self.dialog_pages[self.current_page_index]
            self.ui.draw_dialog(current_text, self.current_page_index, len(self.dialog_pages))

        if self.state == STATE_COMBAT and self.combat:
            # Desenha Arena (opcional, para debug visual)
            # arena_rect = pygame.Rect(SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2 - 150, 400, 300)
            # pygame.draw.rect(self.screen, (30,30,30), arena_rect, 1)
            
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