from random import choice, randint as rnd

import pygame

from src import consts


class Target:
    def __init__(self, screen):
        self.screen = screen
        self.CAT = choice(consts.CATS)
        self.live = 1
        self.tick = 0
        self.finished = False
        self.new_target()
        self.price = 100

    def new_target(self):
        """ Инициализация новой цели. """
        self.tick = 0
        self.live = 1
        self.r = rnd(48, 128)
        self.x = rnd(200, 800 - self.r)
        self.y = rnd(100, 600 - self.r)
        self.finished = False

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.live -= points
        self.tick = 0

    def draw(self):
        if self.finished:
            return
        if self.live > 0:
            frame = (self.tick // 10) % 7
        else:
            frame = min(len(self.CAT) - 1, self.tick // 2)
            if frame == len(self.CAT) - 1:
                self.finished = True
        image = pygame.transform.scale(self.CAT[frame], (self.r, self.r))
        self.screen.blit(image, (self.x, self.y))
        self.tick += 1


class MovingTarget(Target):
    def __init__(self, screen):
        super().__init__(screen)
        pass

