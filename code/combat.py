import pygame
from constants import HEAVY_ATTACK_COOLDOWN

class CombatSystem:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.round = 1
        self.state = "INPUT"   # INPUT, WAIT, ENEMY
        self.actions = ["Ataque Basico", "Ataque Pesado", "Defesa"]
        self.selected = 0
        self.is_defending = False
        self.log = "Início do combate"
        self.finished = False
        self.result = None
        self.wait_timer = 0  # frames to simulate delay

    def handle_input(self, event):
        if self.state != "INPUT" or self.finished:
            return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.selected = (self.selected - 1) % len(self.actions)
            elif event.key == pygame.K_RIGHT:
                self.selected = (self.selected + 1) % len(self.actions)
            elif event.key == pygame.K_RETURN:
                self.player_action()

    def player_action(self):
        action = self.actions[self.selected]
        if action == "Ataque Pesado" and self.player.heavy_cd > 0:
            self.log = "Ataque pesado em cooldown"
            return

        dmg = 0
        self.is_defending = False

        if action == "Ataque Basico":
            dmg = 1
            self.log = "Você usou Ataque Básico"
        elif action == "Ataque Pesado":
            dmg = 2
            self.player.heavy_cd = HEAVY_ATTACK_COOLDOWN + 1
            self.log = "Você usou Ataque Pesado"
        elif action == "Defesa":
            self.is_defending = True
            self.log = "Você está defendendo"

        if dmg > 0:
            self.enemy.hp -= dmg
            if self.enemy.hp <= 0:
                self.enemy.alive = False
                self.finished = True
                self.result = "WIN"
                return

        # passar para turno do inimigo com pequeno delay
        self.state = "WAIT"
        self.wait_timer = 30

    def update(self):
        if self.finished:
            return

        if self.wait_timer > 0:
            self.wait_timer -= 1
            if self.wait_timer == 0:
                # se inimigo ainda vivo, ele ataca
                if self.enemy.alive:
                    self.enemy_turn()
                else:
                    self.finished = True
                    self.result = "WIN"
            return

        # reduzir cooldowns quando volta ao INPUT
        if self.state == "ENEMY":
            # já processado enemy_turn, voltar para input
            self.state = "INPUT"
            self.round += 1
            if self.player.heavy_cd > 0:
                self.player.heavy_cd -= 1

    def enemy_turn(self):
        dmg = self.enemy.damage
        if self.is_defending:
            dmg //= 2
            self.log = f"Inimigo atacou! Dano reduzido para {dmg}"
        else:
            self.log = f"Inimigo atacou! Dano {dmg}"

        self.player.hp -= dmg
        if self.player.hp <= 0:
            self.finished = True
            self.result = "LOSE"
            return

        # fim do turno inimigo
        self.is_defending = False
        self.state = "ENEMY"
