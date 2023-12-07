import math
from random import choice, randint as rnd

import pygame
from pygame.mixer import Sound

import src.consts as consts
from src.buttons import PauseButton, Button
from src.gun import Gun
from src.cats import CatFactory
from src.text_viewer import TextViewer
from src.metal_pipe import MetalPipeBonus

pygame.init()
pygame.font.init()

pause_button = PauseButton(consts.WIDTH - 60, 20, consts.STOP_BUTTON_IMAGE, 0.1)
shop_button = Button(consts.WIDTH - 140, 20, consts.SHOP_BUTTON_IMAGE, 0.1)
buy_button = Button(20, consts.HEIGHT / 2, consts.SHOP_BUY_BUTTON_IMAGE, 1)
exit_button = Button(consts.WIDTH / 2 - 60, consts.HEIGHT - 90, consts.SHOP_EXIT_BUTTON_IMAGE, 1)
# Change cursor
cursor = pygame.transform.scale(consts.CURSOR, (70, 60))

pygame.mouse.set_visible(False)

bullet = 0
balls = []
price = 100

screen = pygame.display.set_mode((consts.WIDTH, consts.HEIGHT))
clock = pygame.time.Clock()
text_view = TextViewer(screen)
gun = Gun(screen, balls)
targets = CatFactory(screen, gun, 4)
metal_pipe = MetalPipeBonus(screen, targets)
finished = False
bullet_type = "rifle"

def show_shop(price):
    font = pygame.font.SysFont('Comic Sans MS', 30)
    pygame.mouse.set_visible(True)
    not_enough_money = None
    while True:
        screen.fill(consts.WHITE)
        charge_gun_price = font.render(f'Увеличить скорость зарядки оружия: {price}', False, (0, 0, 0))
        screen.blit(charge_gun_price, (20, consts.HEIGHT / 2 - 40))

        if not_enough_money is not None:
            screen.blit(not_enough_money, (20, consts.HEIGHT / 2 - 120))

        if buy_button.draw(screen):
            if gun.wallet >= price:
                gun.charge_speed += 0.05
                gun.wallet -= price
                price *= 2
                text_view.on_hit(gun.bullet, gun.wallet)

            else:
                not_enough_money = font.render('У вас не достаточно денег', False, (0, 0, 0))
        if exit_button.draw(screen):
            pygame.mouse.set_visible(False)
            return price

        text_view.draw("Shop")

        if shop_button.draw(screen):
            pygame.mouse.set_visible(False)
            return price

        pause_button.draw(screen)

        pygame.display.update()
        clock.tick(consts.FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True


def set_pause():
    pygame.mouse.set_visible(True)

    while True:
        screen.fill(consts.WHITE)
        text_view.draw("Shop")
        gun.draw()

        for t in targets:
            t.draw()
        for b in balls:
            b.draw()
        if shop_button.draw(screen):
            print("Shop")

        if pause_button.draw(screen):
            pause_button.change_image(consts.STOP_BUTTON_IMAGE, 0.1)
            pygame.mouse.set_visible(False)
            return False

        pygame.display.update()
        clock.tick(consts.FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True


def hit_target(target, ball=None):
    if ball is not None:
        ball.live = 0
    target.hit()
    gun.wallet += target.price
    text_view.on_hit(gun.bullet, gun.wallet)
    gun.bullet = 0

    Sound.play(consts.EXPLOTANO_SOUND)


while not finished:
    screen.fill(consts.WHITE)
    text_view.draw(bullet_type)

    targets.draw()
    gun.draw()
    metal_pipe.draw()

    for b in balls:
        b.draw()

    position = pygame.mouse.get_pos()
    position = (position[0] - 35, position[1] - 30)
    screen.blit(cursor, position)

    if shop_button.draw(screen):
        price = show_shop(price)
    if pause_button.draw(screen):
        pause_button.change_image(consts.PLAY_BUTTON_IMAGE, 0.08)
        finished = set_pause()

    pygame.display.update()
    clock.tick(consts.FPS)

    for t in targets:
        if t.live > 0 and t.hittest(gun):
            hit_target(t)
            break

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)
        elif event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_1]:
                print("riffle")
                gun.change_bullet_type("rifle")
                bullet_type = "rifle"
            elif pygame.key.get_pressed()[pygame.K_2]:
                print("shot_gun")
                gun.change_bullet_type("shotgun")
                bullet_type = "shotgun"

    for b in balls:
        if b.live <= 0:
            balls.remove(b)
            continue

        if metal_pipe.live > 0 and metal_pipe.hittest(b):
            metal_pipe.on_collect()
            b.live = 0
            continue

        for target in targets:
            if target.live > 0 and target.hittest(b):
                hit_target(target, b)
        b.move()

    gun.power_up()

pygame.quit()
