import math
from random import choice, randint as rnd

import pygame
import src.consts as consts
from src.buttons import PauseButton, Button
from src.gun import Gun
from src.target import Target
from src.text_viewer import TextViewer


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

        text_view.draw()

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
        text_view.draw()
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


pygame.init()
pygame.font.init()

print(consts.CATS)

pause_button = PauseButton(consts.WIDTH - 60, 20, consts.STOP_BUTTON_IMAGE, 0.1)
shop_button = Button(consts.WIDTH - 140, 20, consts.SHOP_BUTTON_IMAGE, 0.1)
buy_button = Button(20, consts.HEIGHT / 2, consts.SHOP_BUY_BUTTON_IMAGE, 1)
exit_button = Button(consts.WIDTH / 2 - 60, consts.HEIGHT - 90, consts.SHOP_EXIT_BUTTON_IMAGE, 1)
# Change cursor
cursor = pygame.transform.scale(consts.CURSOR, (70, 60))

pygame.mouse.set_visible(False)

screen = pygame.display.set_mode((consts.WIDTH, consts.HEIGHT))
bullet = 0
balls = []
price = 100
clock = pygame.time.Clock()
text_view = TextViewer(screen)
gun = Gun(screen, balls)
targets = [Target(screen) for i in range(4)]
finished = False

while not finished:
    screen.fill(consts.WHITE)
    text_view.draw()

    gun.draw()

    for t in targets:
        t.draw()
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
            if target.live > 0 and b.hittest(target):
                target.live = 0
                b.live = 0
                target.hit()
                gun.wallet += target.price
                text_view.on_hit(gun.bullet, gun.wallet)
                gun.bullet = 0

    gun.power_up()

pygame.quit()
