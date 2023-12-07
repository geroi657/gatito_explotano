from random import randint as rnd

import pygame


class GenericTarget:
    animation = []
    standby_frames_count = 1

    def __init__(self, screen, gun):
        self.screen = screen
        self.gun = gun # для самонаведения, ы
        self.tick = 0
        self.live = 1
        self.finished = False
        self.r = rnd(48, 128)
        self.x = rnd(400, 800 - self.r)
        self.y = rnd(100, 600 - self.r)
        self.step = rnd(2, 4)
        self.price = 100

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.live -= points
        self.tick = 0

    def move(self):
        # Работаем каждый второй фрейм
        if self.tick % 2 != 0 or self.live < 1:
            return

        # О НЕТ ДЖОННИ ОНИ НА ДЕРЕВЬЯХ
        step = self.step
        if self.gun.x < self.x:
            self.x -= round(step / 2)
            step = round(step / 2)
        elif self.gun.x > self.x:
            self.x += round(step / 2)
            step = round(step / 2)
        if self.gun.y < self.y:
            self.y -= step
        elif self.gun.y > self.y:
            self.y += step

    def draw(self):
        if self.finished:
            return
        if self.live > 0:
            frame = (self.tick // 10) % self.standby_frames_count
        else:
            frame = min(len(self.animation) - 1, self.tick // 2)
            if frame == len(self.animation) - 1:
                self.finished = True
        image = pygame.transform.scale(self.animation[frame], (self.r, self.r))
        self.screen.blit(image, (self.x, self.y))
        self.tick += 1
