import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_fleet import AlienFleet

class Sprinter(Sprite):

    """Manages different functions that need to be run for each individual alien"""

    def __init__(self, fleet:'AlienFleet', x: float, y: float):
        
        """Initializes the art and all needed variables"""

        super().__init__()

        self.screen = fleet.game.screen
        self.boundaries = fleet.game.screen.get_rect()
        self.settings = fleet.game.settings

        self.fleet = fleet

        self.image = pygame.image.load(self.settings.sprinter_file)
        self.image = pygame.transform.scale(self.image, (self.settings.alien_w, self.settings.alien_h))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

    def update(self):
        
        """Updates the current position of the sprinter"""

        self.y += self.settings.sprinter_speed
        
        self.rect.y = self.y

    def check_edges(self):

        """Checks if this alien is touching the sides of the screen"""

        return (self.rect.right >= self.boundaries.right or self.rect.left <= self.boundaries.left)


    def draw_alien(self):

        """Redraws the sprinter at its new position"""
        
        self.screen.blit(self.image, self.rect)