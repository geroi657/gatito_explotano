import math
from random import choice, randint as rnd

import pygame


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

WIDTH = 800
HEIGHT = 600

TANK_SPRITE = pygame.image.load("tank.png")
TANK_SIZE = 49

CAT = [pygame.image.load(f"cat/{i}.png") for i in range(1, 25)]
CAT_SIZE = 128

def between(a, x, b):
    return max(a, min(x, b))

class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
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
        self.color = choice(GAME_COLORS)
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
            self.vx = -self.vx - 5
        if self.y <= 0 or self.y  >= edge_y:
            self.vy = -self.vy - 5
        self.live -= 1

    def draw(self):
        if self.live <= 0:
            return
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        return self.x > obj.x \
            and self.y > obj.y \
            and self.x < obj.x + obj.r \
            and self.y < obj.y + obj.r


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.x = 40
        self.y = 450
        self.rotation = 3
        self.an = 1
        self.color = GREY

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        # фу какая гадость, нас учать юзать глоб переменные что-ли
        # поправьте если кому не лень
        bullet += 1
        new_ball = Ball(self.screen, self.x + TANK_SIZE / 2, self.y + TANK_SIZE / 2)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.pos[1]-450) / max(1, event.pos[0]-20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        # FIXIT don't know how to do it
        tank = pygame.transform.rotate(TANK_SPRITE, 90 * self.rotation)
        self.screen.blit(tank, (self.x, self.y))

        # Draw muzzle
        w = 9 + round(self.f2_power / 30)
        l = 50 + round(self.f2_power / 2)
        sx = self.x + TANK_SIZE / 2 - 10
        sy = self.y + TANK_SIZE / 2
        ex = sx + l * math.cos(self.an)
        ey = sy + l * math.sin(self.an)
        pygame.draw.line(self.screen, self.color, (sx, sy), (ex, ey), w)
        pygame.draw.circle(self.screen, self.color, (ex, ey), w / 1.5)

    def power_up(self):
        self.color = GREY
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            else:
                self.color = RED


class Target:
    def __init__(self, screen):
        self.screen = screen
        self.live = 1
        self.tick = 0
        self.finished = False
        self.new_target()

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
            frame = min(len(CAT) - 1, self.tick // 2)
            if frame == len(CAT) - 1:
                self.finished = True
        image = pygame.transform.scale(CAT[frame], (self.r, self.r))
        self.screen.blit(image, (self.x, self.y))
        self.tick += 1


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
score = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
targets = [Target(screen) for i in range(4)]
finished = False

while not finished:
    screen.fill(WHITE)
    gun.draw()
    for t in targets:
        t.draw()
    for b in balls:
        b.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for target in targets:
        if target.finished:
            target.new_target()

    for b in balls:
        b.move()
        if b.live <= 0:
            balls.remove(b)
        for target in targets:
            if b.hittest(target) and target.live:
                target.live = 0
                b.live = 0
                target.hit()
                score += 1
    gun.power_up()

pygame.quit()
