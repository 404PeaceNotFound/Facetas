import pygame

FILES = {
    "menu_music": "code/assets/sfx/menu_music2.mp3",
    "level_music": "code/assets/sfx/level_music.mp3",
    "sfx_attack": "code/assets/sfx/soco_fraco.mp3",
    "sfx_heavy": "code/assets/sfx/soco.mp3",
    "sfx_enemy": "code/assets/sfx/ataque_mob.mp3",
    "sfx_victory": "code/assets/sfx/victory.mp3",
}

_sfx = {}
_initialized = False

def init_audio():
    global _initialized
    if _initialized:
        return
    try:
        pygame.mixer.init()
    except Exception:
        _initialized = False
        return
    
    for key in ("sfx_attack", "sfx_heavy", "sfx_enemy", "sfx_victory"):
        path = FILES.get(key)
        try:
            _sfx[key] = pygame.mixer.Sound(path)
        except Exception:
            _sfx[key] = None
    _initialized = True

# Música de fundo (usa pygame.mixer.music para loop)
def play_menu_music():
    if not _initialized: return
    try:
        pygame.mixer.music.load(FILES["menu_music"])
        pygame.mixer.music.play(-1)  # loop infinito
    except Exception:
        pass

def play_level_music():
    if not _initialized: return
    try:
        pygame.mixer.music.load(FILES["level_music"])
        pygame.mixer.music.play(-1)
    except Exception:
        pass

def stop_music():
    if not _initialized: return
    pygame.mixer.music.stop()

def play_sfx(name):
    if not _initialized: return
    s = _sfx.get(name)
    if s:
        s.play()
