import pygame
import sys
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
        self.running = True
        self.state = STATE_MENU
        
        # Inicialização
        self.init_game_objects()
        
        # Menu
        self.menu_options = ["Start", "Creditos"]
        self.menu_index = 0

    def init_game_objects(self):
        self.player = Player()
        self.map = GameMap()
        self.camera = Camera()
        
        # Inimigos: 2 comuns, 1 boss
        self.enemies = [
            Enemy(600),          # Inimigo 1
            Enemy(1200),         # Inimigo 2
            Enemy(1800, is_boss=True) # Boss
        ]
        
        # NPC
        self.npcs = [
            NPC(300, "Cuidado! Inimigos a frente.")
        ]
        
        self.combat_sys = None
        self.active_dialog = None
        self.dialog_active = False
        self.victory_count = 0

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            
            # Input Global
            if self.state == STATE_MENU:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.menu_index = (self.menu_index - 1) % len(self.menu_options)
                    elif event.key == pygame.K_DOWN:
                        self.menu_index = (self.menu_index + 1) % len(self.menu_options)
                    elif event.key == pygame.K_RETURN:
                        if self.menu_index == 0:
                            self.init_game_objects()
                            self.state = STATE_EXPLORE
                        else:
                            self.state = STATE_CREDITS

            elif self.state == STATE_CREDITS:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    # self.running = Fal
                    self.state = STATE_MENU

            elif self.state == STATE_EXPLORE:
                pass

            elif self.state == STATE_DIALOG:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                    self.state = STATE_EXPLORE
                    self.active_dialog = None
                    self.dialog_active = True # isso significa que o diálogo já aconteceu

            elif self.state == STATE_COMBAT:
                self.combat_sys.handle_input(event)

            elif self.state == STATE_GAME_OVER or self.state == STATE_VICTORY:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.state = STATE_MENU

    def update(self):
        if self.state == STATE_EXPLORE:
            self.player.update()
            self.camera.update(self.player.rect)

            # Checar colisão NPC
            for npc in self.npcs:
                if self.player.rect.colliderect(npc.rect):
                    
                    # caso o diálogo já tenha aparecido, ele não vai aparecer mais 
                    if not self.dialog_active:
                        self.state = STATE_DIALOG
                        self.active_dialog = npc.text
            
            # Checar colisão Inimigo (Trigger Combate)
            for enemy in self.enemies:
                if enemy.alive and self.player.rect.colliderect(enemy.rect):
                    self.start_combat(enemy)
                    break

        elif self.state == STATE_COMBAT:
            self.combat_sys.update()
            if self.combat_sys.finished:
                if self.combat_sys.result == "WIN":
                    self.combat_sys.enemy.alive = False
                    self.victory_count += 1
                    if self.combat_sys.enemy.is_boss:
                         self.state = STATE_VICTORY
                    else:
                         self.state = STATE_EXPLORE
                else:
                    self.state = STATE_GAME_OVER

    def start_combat(self, enemy):
        self.state = STATE_COMBAT
        # Centraliza camera na arena
        self.camera.center_on_arena(enemy.rect.centerx)
        self.combat_sys = CombatSystem(self.player, enemy)

    def draw(self):
        if self.state == STATE_MENU:
            self.ui.draw_menu(self.menu_options, self.menu_index)
        
        elif self.state == STATE_CREDITS:
            self.screen.fill(BLACK)
            self.ui.draw_text("Desenvolvido por:", "big", 50, 50)
            self.ui.draw_text("Game Design: Thiago & Dudu", "small", 50, 150)
            self.ui.draw_text("Game Dev   : Yuri & Vitor", "small", 50, 200)
            self.ui.draw_text("Pressione ENTER para Sair", "small", 50, 500, RED)

        elif self.state in [STATE_EXPLORE, STATE_DIALOG, STATE_COMBAT]:
            self.screen.fill(BLACK)
            self.map.draw(self.screen, self.camera.offset_x)
            
            for npc in self.npcs:
                npc.draw(self.screen, self.camera.offset_x)
            
            for enemy in self.enemies:
                enemy.draw(self.screen, self.camera.offset_x)
                
            self.player.draw(self.screen, self.camera.offset_x)

            if self.state == STATE_DIALOG:
                self.ui.draw_dialog(self.active_dialog)
            
            if self.state == STATE_COMBAT:
                self.ui.draw_combat_hud(
                    self.player.hp, 
                    self.combat_sys.enemy.hp, 
                    self.combat_sys.round,
                    self.combat_sys.log,
                    self.combat_sys.actions,
                    self.combat_sys.selected_action,
                    self.player.heavy_cd
                )

        elif self.state == STATE_GAME_OVER:
            self.screen.fill(BLACK)
            self.ui.draw_text("GAME OVER", "big", SCREEN_WIDTH//2, SCREEN_HEIGHT//2, RED, center=True)
            self.ui.draw_text("Enter p/ Menu", "small", SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50, center=True)

        elif self.state == STATE_VICTORY:
            self.screen.fill(WHITE) # Flash branco ou fundo claro
            self.ui.draw_text("VITORIA!", "big", SCREEN_WIDTH//2, SCREEN_HEIGHT//2, BLACK, center=True)
            self.ui.draw_text("Enter p/ Menu", "small", SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50, BLACK, center=True)

        pygame.display.flip()