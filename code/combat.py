import pygame
from constants import HEAVY_ATTACK_COOLDOWN, STATE_COMBAT, WHITE, GREEN
from audio import play_sfx

class CombatSystem:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.round = 1
        self.state = "INPUT"   # INPUT, WAIT, ENEMY
        self.actions = ["Ataque Básico", "Ataque Pesado", "Defesa"]
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

        if action == "Ataque Básico":
            dmg = 1
            self.log = "Você usou Ataque Básico"
            # SFX ataque normal
            play_sfx("sfx_attack")
        elif action == "Ataque Pesado":
            dmg = 2
            self.player.heavy_cd = HEAVY_ATTACK_COOLDOWN
            self.log = "Você usou Ataque Pesado"
            # SFX ataque pesado
            play_sfx("sfx_heavy")
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

        self.state = "WAIT"
        self.wait_timer = 30

    def update(self):
        if self.finished:
            return

        if self.wait_timer > 0:
            self.wait_timer -= 1
            if self.wait_timer == 0:
                if self.enemy.alive:
                    self.enemy_turn()
                else:
                    self.finished = True
                    self.result = "WIN"
            return

        if self.state == "ENEMY":
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

        play_sfx("sfx_enemy")

        self.player.hp -= dmg
        if self.player.hp <= 0:
            self.finished = True
            self.result = "LOSE"
            return

        self.is_defending = False
        self.state = "ENEMY"

    def start_combat(self, enemy):
        if not enemy.alive:
            return
        self.state = STATE_COMBAT
        self.camera.center_on(enemy.rect.centerx)
        self.combat = CombatSystem(self.player, enemy)

        arena_center_x = enemy.rect.centerx
        arena_y = enemy.rect.y
        self.player.rect.midright = (arena_center_x - 100, arena_y + 50)
        enemy.rect.midleft = (arena_center_x + 100, arena_y + 50)

    def draw(self, screen, cam_x):
        arena_w, arena_h = 400, 300
        center_x = self.enemy.rect.centerx + cam_x
        center_y = self.enemy.rect.centery
        arena = pygame.Rect(center_x - arena_w//2, center_y - arena_h//2, arena_w, arena_h)
        pygame.draw.rect(screen, (60,60,80), arena)
        pygame.draw.rect(screen, WHITE, arena, 2)

        p_rect = pygame.Rect(arena.x + 50, arena.centery - 30, 40, 60)
        e_rect = pygame.Rect(arena.right - 90, arena.centery - 30, 40, 60)

        pygame.draw.rect(screen, GREEN, p_rect)
        pygame.draw.rect(screen, self.enemy.color, e_rect)

        # HUD
        try:
            self.game.ui.draw_combat_hud(
                self.player.hp, self.enemy.hp, self.round,
                self.log, self.actions, self.selected, self.player.heavy_cd
            )
        except Exception:
            pass
