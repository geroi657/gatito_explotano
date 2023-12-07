import pygame
from pygame.mixer import Sound, init as mixer_init

mixer_init()

FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
EXPLOTANO_SOUND = Sound("assets/explotano.ogg")

TANK_SPRITE = pygame.image.load("assets/tank.png")
TANK_SIZE = 49

BONUS_SPRITE = pygame.image.load("assets/bonus.png")
BONUS_SIZE = 64

METAL_PIPE_SPRITE = pygame.image.load("assets/metal_pipe.png")
METAL_PIPE_SIZE = 496, 240

WIDTH = 800
HEIGHT = 600

CAT_ANIMATIONS = [[pygame.image.load(f"assets/cat_0/{i}.png") for i in range(1, 25)],
                 [pygame.image.load(f"assets/cat_1/{i}.png") for i in range(1, 21)],
                 [pygame.image.load(f"assets/cat_2/{i}.png") for i in range(1, 24)]]


CAT_SIZE = 128

STOP_BUTTON_IMAGE = pygame.image.load('assets/StopButton.png')
PLAY_BUTTON_IMAGE = pygame.image.load('assets/PlayButton.png')
SHOP_BUTTON_IMAGE = pygame.image.load('assets/cart.png')
CURSOR = pygame.image.load('assets/Aim.png')
SHOP_BUY_BUTTON_IMAGE = pygame.image.load('assets/buy_button.png')
SHOP_EXIT_BUTTON_IMAGE = pygame.image.load('assets/exit_button.png')
