import math

import pygame

from src import consts
from src.ball import Ball


class Gun:
    def __init__(self, screen, balls):
        self.charge_speed = 1
        self.screen = screen
        self.bullet = 0
        self.balls = balls
        self.f2_power = 10
        self.f2_on = 0
        self.x = 40
        self.y = 450
        self.r = 4  # для детектора коллизий
        self.rotation = 6
        self.an = 1
        self.color = consts.GREY
        self.wallet = 0
        self.max_power = 100
        self.bullet_amount = 1
        self.bullet_size = 5

    def change_bullet_type(self, _type="rifle"):
        if _type == "rifle":
            self.max_power = 100
            self.charge_speed = 1
            self.bullet_amount = 1
            self.bullet_size = 5
        elif _type == "shotgun":
            self.max_power = 10
            self.charge_speed = 20
            self.bullet_amount = 3
            self.bullet_size = 0

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        if self.bullet_amount > 1:
            self.create_bullet(event, 15)
            self.create_bullet(event, 0)
            self.create_bullet(event, -15)
        else:
            self.create_bullet(event, 0)

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.pos[1]) / max(1, event.pos[0] - 20))
        if self.f2_on:
            self.color = consts.RED
        else:
            self.color = consts.GREY

    def create_bullet(self, event, vector_change=1):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        self.bullet += 1
        new_ball = Ball(self.screen, consts.GAME_COLORS, self.x + consts.TANK_SIZE / 2, self.y + consts.TANK_SIZE / 2)
        new_ball.r += self.bullet_size
        self.an = math.atan2((event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an) + vector_change
        self.balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def draw(self):
        # FIXIT don't know how to do it
        tank = pygame.transform.rotate(consts.TANK_SPRITE, 45 * self.rotation)
        self.screen.blit(tank, (self.x, self.y))

        # Draw muzzle
        w = 9 + round(self.f2_power / 30)
        l = 50 + round(self.f2_power / 2)
        sx = self.x + consts.TANK_SIZE / 2
        sy = self.y + consts.TANK_SIZE / 2
        ex = sx + l * math.cos(self.an)
        ey = sy + l * math.sin(self.an)
        pygame.draw.line(self.screen, self.color, (sx, sy), (ex, ey), w)
        pygame.draw.circle(self.screen, self.color, (ex, ey), w / 1.5)

    def power_up(self):
        self.color = consts.GREY
        if self.f2_on:
            if self.f2_power < self.max_power:
                self.f2_power += self.charge_speed
            else:
                self.color = consts.RED
