import pygame

class TextViewer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.font2 = pygame.font.SysFont('Comic Sans MS', 20)

        self.score = 0
        self.score_info = self.font.render(f'Счёт: {self.score}', False, (0, 0, 0))
        self.wallet_info = self.font.render('Кошелек: 0$', False, (0, 0, 0))
        self.hit_info = None
        self.tick = 0

    def on_hit(self, bullet, wallet):
        self.score += 1
        self.score_info = self.font.render(f'Счёт: {self.score}', False, (0, 0, 0))
        self.wallet_info = self.font.render(f'Кошелек: {wallet}$', False, (0, 0, 0))

        self.hit_info = self.font2.render(f"Вы попали, потратив {bullet} ракет!", False, (0, 255, 0))
        self.tick = 60

    def draw(self):
        self.screen.blit(self.score_info, (20, 20))
        self.screen.blit(self.wallet_info, (120, 20))

        if self.tick > 0:
            self.screen.blit(self.hit_info, (20, 60))
            self.tick -= 1
