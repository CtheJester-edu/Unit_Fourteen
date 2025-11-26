import random
import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Round2(Sprite):

    """Manages all round specific functions"""

    def __init__(self, game:'AlienInvasion'):

        """Initializes the art and all needed variables"""

        super().__init__()

        self.screen = game.screen
        self.settings = game.settings

        self.image = pygame.image.load(self.settings.round_file)
        self.image = pygame.transform.scale(self.image, (self.settings.round_w, self.settings.round_h))

        self.rect = self.image.get_rect()

        self.rect.midtop = game.ship.rect.topright

        self.y = float(self.rect.y)

    def update(self):
        
        """Moves the round up the screen"""

        self.y -= self.settings.round_speed
        self.rect.y = self.y

    def draw_round(self):

        """Updates the round to its new position"""
        
        self.screen.blit(self.image, self.rect)