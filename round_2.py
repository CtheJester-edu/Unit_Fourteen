import random
import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Round2(Sprite):

    def __init__(self, game:'AlienInvasion'):
        super().__init__()

        self.screen = game.screen
        self.settings = game.settings

        self.image = pygame.image.load(self.settings.round_file)
        self.image = pygame.transform.scale(self.image, (self.settings.round_w, self.settings.round_h))

        self.rect = self.image.get_rect()
        
        #trying something
        #self.side = random.choic(['left', 'right'])
        #self.rect.midtop = game.ship.rect.(self.side)
        #self.rect.midtop = game.ship.rect.midtop

        self.rect.midtop = game.ship.rect.topright

        self.y = float(self.rect.y)

    def update(self):
        self.y -= self.settings.round_speed
        self.rect.y = self.y

    def draw_round(self):
        self.screen.blit(self.image, self.rect)