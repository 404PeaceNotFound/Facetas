import pygame
from constants import *

class CombatSystem:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.round = 1
        self.turn = "PLAYER" # PLAYER ou ENEMY
        self.log = "Inicio do Combate!"
        self.actions = ["Ataque Basico", "Ataque Pesado", "Defesa"]
        self.selected_action = 0
        self.is_defending = False
        self.finished = False
        self.result = None # 'WIN' ou 'LOSE'
        
        # Timer simples para feedback
        self.feedback_timer = 0
        self.state = "INPUT" # INPUT, ANIMATION, ENEMY_TURN

    def update(self):
        if self.feedback_timer > 0:
            self.feedback_timer -= 1
            if self.feedback_timer == 0:
                if self.state == "ANIMATION":
                    self.end_player_turn()
                elif self.state == "ENEMY_TURN":
                    self.enemy_action()
            return

    def handle_input(self, event):
        if self.state != "INPUT": return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.selected_action = (self.selected_action - 1) % len(self.actions)
            elif event.key == pygame.K_RIGHT:
                self.selected_action = (self.selected_action + 1) % len(self.actions)
            elif event.key == pygame.K_RETURN:
                self.execute_player_action()

    def execute_player_action(self):
        action = self.actions[self.selected_action]
        
        if action == "Ataque Pesado" and self.player.heavy_cd > 0:
            self.log = "Habilidade em Cooldown!"
            return

        damage = 0
        self.is_defending = False

        if action == "Ataque Básico":
            damage = 1
            self.log = "Você usou Ataque Básico!"
        elif action == "Ataque Pesado":
            damage = 2
            self.player.heavy_cd = HEAVY_ATTACK_COOLDOWN + 1 # +1 pois decrements no fim do round
            self.log = "Você usou Ataque Pesado!"
        elif action == "Defesa":
            self.is_defending = True
            self.log = "Você está defendendo!"

        if damage > 0:
            self.enemy.hp -= damage
            # Flash effect simulated by changing log

        self.state = "ANIMATION"
        self.feedback_timer = 30 # 1 segundo de espera

    def end_player_turn(self):
        if self.enemy.hp <= 0:
            self.finished = True
            self.result = "WIN"
            return
        
        self.state = "ENEMY_TURN"
        self.log = "Turno do Inimigo..."
        self.feedback_timer = 30

    def enemy_action(self):
        dmg = self.enemy.damage
        if self.is_defending:
            dmg //= 2
            self.log = f"Inimigo atacou! Dano reduzido para {dmg}."
        else:
            self.log = f"Inimigo atacou! Dano {dmg}."

        self.player.hp -= dmg
        
        if self.player.hp <= 0:
            self.finished = True
            self.result = "LOSE"
            return

        # Fim do round
        self.round += 1
        if self.player.heavy_cd > 0:
            self.player.heavy_cd -= 1
        
        self.state = "INPUT"
        self.turn = "PLAYER"