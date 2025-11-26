import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    from arsenal import Arsenal

class Ship:

    """Creates and Manages all operations for the Ship"""

    def __init__(self, game: 'AlienInvasion', arsenal: 'Arsenal'):

        """Establishes Base Ship Settings and Variables"""

        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.boundaries = self.screen.get_rect()

        self.image = pygame.image.load(self.settings.ship_file)
        self.image = pygame.transform.scale(self.image, (self.settings.ship_w, self.settings.ship_h))

        self.rect = self.image.get_rect()
        self._center_ship()

        self.moving_right = False
        self.moving_left = False
        self.x = float(self.rect.x)

        self.arsenal = arsenal

        self.spin = False
        self.r = float(0)

        self.moving_up = False
        self.moving_down = False
        self.y = float(self.rect.y)

    def _center_ship(self):

        """Resets the ship for new rounds"""

        self.rect.midbottom = self.boundaries.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):

        """Updates the ship to move it and all shots on the screen"""

        self._update_ship_movement()
        self.arsenal.update_arsenal()

    def _update_ship_movement(self):

        """Moves the ship in coordination with key down and key up events"""

        if self.moving_right and self.rect.right < self.boundaries.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > self.boundaries.left:
            self.x -= self.settings.ship_speed
        if self.spin:
            self.r += 5
        if self.moving_up and self.rect.top > self.boundaries.top:
            self.y -= self.settings.ship_speed_vertical
        if self.moving_down and self.rect.bottom < self.boundaries.bottom:
            self.y += self.settings.ship_speed_vertical
        

        self.rect.x = self.x
        self.image = pygame.transform.rotate(self.image, self.r)
        self.rect.y = self.y

    def draw(self):

        """Draws the ship and all shots on the screen"""

        self.arsenal.draw()
        self.screen.blit(self.image, self.rect)

    def fire(self):

        """Fires the Main Gun"""

        return self.arsenal.fire_bullet()
    
    def fire_cannon1(self):

        """Fires the 1st secondary gun"""

        return self.arsenal.fire_round1()
    
    def fire_cannon2(self):
        
        """Fires the 2nd secondary gun"""

        return self.arsenal.fire_round2()
    
    def check_collisions(self, other_group):

        """Checks collision with whatever sprite group is fed into it"""
        
        if pygame.sprite.spritecollideany(self, other_group):
            self._center_ship()
            return True
        else:
            return False