import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    #bullet class and methods

    def __init__(self, sd_game):
        super().__init__()
        self.screen = sd_game.screen
        self.settings = sd_game.settings
        self.color = self.settings.bullet_color

        #create bullet at 0,0
        self.rect = pygame.Rect(0,0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = sd_game.ship.rect.midtop
        self.settings.bullet_sound.play()

        #store bullet
        self.y = float(self.rect.y)
    def update(self):
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect) 