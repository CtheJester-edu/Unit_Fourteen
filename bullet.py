import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Bullet(Sprite):

    """Manages the updating and drawing of bullets"""

    def __init__(self, game:'AlienInvasion'):

        """Sets up all needed stats and variables needed for each bullet"""

        super().__init__()

        self.screen = game.screen
        self.settings = game.settings

        self.image = pygame.image.load(self.settings.bullet_file)
        self.image = pygame.transform.scale(self.image, (self.settings.bullet_w, self.settings.bullet_h))

        self.rect = self.image.get_rect()
        self.rect.midtop = game.ship.rect.midtop
        self.y = float(self.rect.y)

    def update(self):

        """Moves the bullet up the screen"""

        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):

        """Draws the Bullet in its new position"""
        
        self.screen.blit(self.image, self.rect)