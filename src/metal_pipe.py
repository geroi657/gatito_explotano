import pygame
from pygame.mixer import Sound
from random import randint as rnd

from src.consts import BONUS_SIZE, BONUS_SPRITE, METAL_PIPE_SIZE, METAL_PIPE_SPRITE, WIDTH

class MetalPipeBonus:
    def __init__(self, screen, targets):
        self._targets = targets
        self._screen = screen
        self._started = False
        self.x = -600
        self.y = -600
        self.r = BONUS_SIZE
        self.live = 0
        self.tick = 0

        self.sound = Sound("assets/pipe.ogg")

    def draw(self):
        if self._started:
            self._draw_animation()
        elif self.live > 0:
            self._draw_collectable()
        elif self.tick == 600:
            self._show_bonus()
            self.tick = 0
        self.tick += 1

    def _show_bonus(self):
        self.x = rnd(400, 700)
        self.y = rnd(100, 600)
        self.live = 1

    def on_collect(self):
        self.live = 0
        self.tick = 0
        self._started = True

    def _draw_collectable(self):
        self._screen.blit(BONUS_SPRITE, (self.x, self.y))

    def _draw_animation(self):
        w, h = METAL_PIPE_SIZE
        x = round((WIDTH - w) / 2)
        y = 3 * min(self.tick, 60)
        self._screen.blit(METAL_PIPE_SPRITE, (x, y))

        if self.tick == 60:
            Sound.play(self.sound)
            for t in self._targets:
                t.hit()

        if self.tick == 90:
            self._started = False

    def hittest(self, obj):
        return obj.x > self.x \
            and obj.y > self.y \
            and obj.x < self.x + self.r \
            and obj.y < self.y + self.r
