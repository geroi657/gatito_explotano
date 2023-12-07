import pygame


class TextViewer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.font2 = pygame.font.SysFont('Comic Sans MS', 20)

        self.score = 0
        self.score_info = self.font.render(f'Счёт: {self.score} Кошелек: 0$', False, (0, 0, 0))
        self.rifle_bullet = self.font.render(f"1. Винтовка", False, (0, 255, 0))
        self.shotgun_bullet = self.font.render(f"2. Дрободык", False, (0, 0, 0))
        self.hit_info = None
        self.tick = 0

    def on_hit(self, bullet, wallet):
        self.score += 1
        self.score_info = self.font.render(f'Счёт: {self.score} Кошелек: {wallet}$', False, (0, 0, 0))
        self.hit_info = self.font2.render(f"Вы попали, потратив {bullet} ракет!", False, (0, 255, 0))
        self.tick = 60

    def draw(self, bullet_type):
        self.screen.blit(self.score_info, (20, 20))

        if bullet_type == 'rifle':
            self.rifle_bullet = self.font.render(f"1. Винтовка", False, (0, 255, 0))
            self.shotgun_bullet = self.font.render(f"2. Дрободык", False, (0, 0, 0))

        elif bullet_type == 'shotgun':
            self.shotgun_bullet = self.font.render(f"2. Дрободык", False, (0, 255, 0))
            self.rifle_bullet = self.font.render(f"1. Винтовка", False, (0, 0, 0))
        if bullet_type != "Shop":
            self.screen.blit(self.rifle_bullet, (20, 90))
            self.screen.blit(self.shotgun_bullet, (20, 130))

        if self.tick > 0:
            self.screen.blit(self.hit_info, (20, 60))
            self.tick -= 1
