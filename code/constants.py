import os

# Isso pega o caminho da pasta onde o jogo está rodando
BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../")

def get_asset_path(relative_path):
    return os.path.join(BASE_DIR, relative_path)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 30
TITLE = "Facetas"

# Mapa
MAP_WIDTH = 2000
MAP_HEIGHT = 600

# Cores usadas
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (50, 50, 50)

# Estados do jogo (valores simples e suficientes)
STATE_MENU = 0
STATE_EXPLORE = 1
STATE_COMBAT = 2
STATE_CREDITS = 3
STATE_GAME_OVER = 4
STATE_DIALOG = 5

# Gameplay
PLAYER_SPEED = 5
PLAYER_MAX_HP = 100
HEAVY_ATTACK_COOLDOWN = 2

STATE_INTRO1 = "intro1"
STATE_INTRO2 = "intro2"