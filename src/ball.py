import pygame
from random import choice, randint as rnd
def between(a, x, b):
    return max(a, min(x, b))

class Ball:
    def __init__(self, screen: pygame.Surface, game_colors, x=40, y=450, ):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(game_colors)
        self.live = 120

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        if self.live <= 0:
            return
        edge_x = 800 - self.r * 2
        edge_y = 600 - self.r * 2
        self.x = between(0, self.x + self.vx, edge_x)
        self.y = between(0, self.y - self.vy, edge_y)
        self.vy -= 1
        if self.x <= 0 or self.x >= edge_x:
            self.vx = -self.vx - 10
        if self.y <= 0 or self.y >= edge_y:
            self.vy = -self.vy - 10
        self.live -= 1

    def draw(self):
        if self.live <= 0:
            return
        pygame.draw.circle(
            self.screen,
            self.color,
            (round(self.x), round(self.y)),
            round(self.r)
        )
