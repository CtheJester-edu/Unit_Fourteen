import pygame
from alien import Alien
from typing import TYPE_CHECKING
from sprinter import Sprinter

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class AlienFleet:

    """This class establishes and manages the alien and special fleet sprite groups"""

    def __init__(self, game:"AlienInvasion"):

        """This function initializes the sprite groups for the aliens and other settings as needed"""

        self.game = game
        self.settings = game.settings
        self.stats = game.game_stats
       
        self.fleet = pygame.sprite.Group()
        self.special = pygame.sprite.Group()
        
        self.fleet_direction = self.settings.fleet_direction
        self.fleet_drop = self.settings.fleet_drop_speed

        self.create_fleet()

    def create_fleet(self):

        """
        Initializes and finds the alien placement box.
        Runs the create fleet function.
        Runs the function to increase some difficulty.
        """

        alien_w = self.settings.alien_w
        alien_h = self.settings.alien_h
        screen_w = self.settings.screen_w
        screen_h = self.settings.screen_h

        fleet_w, fleet_h = self.calculate_fleet_size(alien_w, screen_w, alien_h, screen_h)

        x_offset, y_offset = self.calculate_offset(alien_w, alien_h, screen_w, fleet_w, fleet_h)

        self._create_rectangle_fleet(alien_w, alien_h, fleet_w, fleet_h, x_offset, y_offset)
        if self.stats.level > 5:
            self.speedy(alien_w, alien_h, fleet_w, fleet_h, x_offset, y_offset)

    def speedy(self, alien_w, alien_h, fleet_w, fleet_h, x_offset, y_offset):
         
        """Creates the speedy fleet for sprinters adding them to the special sprite group"""

        for col in range(fleet_w):
                current_x = alien_w * col + x_offset
                current_y = alien_h + y_offset
                if col % 2 == 0:
                    continue
                self._create_sprinter(current_x, current_y)


    def _create_rectangle_fleet(self, alien_w, alien_h, fleet_w, fleet_h, x_offset, y_offset):

        """Creates the Fleet of Aliens adding them to the fleet sprite group"""

        for row in range(fleet_h):
            for col in range(fleet_w):
                current_x = alien_w * col + x_offset
                current_y = alien_h * row + y_offset
                if col % 2 == 0 or row % 2 == 0:
                    continue

                self._create_alien(current_x, current_y)

    def calculate_offset(self, alien_w, alien_h, screen_w, fleet_w, fleet_h):

        """Calculates the side to side offset for the main alien fleet"""

        fleet_pixel_w = fleet_w * alien_w
        x_offset = int((screen_w - fleet_pixel_w)//2)

        fleet_pixel_h = fleet_h * alien_h
        half_screen = self.settings.screen_h//2
        y_offset = int((half_screen - fleet_pixel_h)//2)
        return x_offset,y_offset


    def calculate_fleet_size(self, alien_w, screen_w, alien_h, screen_h):

        """
        Calculates how many aliens wide and tall the alien fleet is.
        Returns the number of aliens to go in each direction as an int.
        """
        fleet_w = (screen_w//alien_w)
        fleet_h = ((screen_h/2)//alien_h)

        if fleet_w % 2 == 0:
            fleet_w -= 1
        else:
            fleet_w -= 2

        if fleet_h % 2 == 0:
            fleet_h -= 1
        else:
            fleet_h -= 2
        
        return int(fleet_w), int(fleet_h)
    
    def _create_alien(self, current_x: int, current_y: int):

        """Creates and new alien in the fleet sprite group at whatever coords it recieces"""

        new_alien = Alien(self, current_x, current_y)
        self.fleet.add(new_alien)

    def _create_sprinter(self, current_x: int, current_y: int):

        """Creates and new sprinter in the special sprite group at whatever coords it recieces"""
        
        new_alien = Sprinter(self, current_x, current_y)
        self.special.add(new_alien)

    def _check_fleet_edges(self):

        """Checks if the alien fleet is touching the game boundaries and drops them down if needed"""

        alien: 'Alien'
        for alien in self.fleet:
            if alien.check_edges():
                self._drop_alien_fleet()
                self.fleet_direction *= (-1)
                break
    
    def _drop_alien_fleet(self):

        """Drops all aliens down"""

        for alien in self.fleet:
            alien.y += self.settings.fleet_drop_speed

    def update_fleet(self):

        """Runs the sprite update functions and the check edges functions for all aliens"""

        self._check_fleet_edges()
        self.fleet.update()
        self.special.update()

    def draw_fleet(self):

        """"Draws all aliens in the fleet and special fleet"""
        alien: 'Alien'
        for alien in self.fleet:
            alien.draw_alien()
        for alien in self.special:
            alien.draw_alien()

    def check_cannon_collisions(self, other_group):

        """Checks collisions for aliens and the cannon rounds"""

        return pygame.sprite.groupcollide(self.fleet, other_group, True, False)
    
    def check_round_collisions(self, other_group):

        """Checks collisions for aliens and the secondary weapon rounds"""

        return pygame.sprite.groupcollide(self.fleet, other_group, True, True)
    
    def check_special_round_collisions(self, other_group):

        """Checks collisions for special aliens and the secondary weapon rounds"""

        return pygame.sprite.groupcollide(self.special, other_group, True, True)
    
    def check_special_cannon_collisions(self, other_group):

        """Checks collisions for special aliens and the cannon rounds"""

        return pygame.sprite.groupcollide(self.special, other_group, True, False)
    
    """def check_fleet_bottom(self):

    
        Checks for each alien if they are touching the bottom of the screen.
        If they are they are sent to the top of the screen.


        alien: 'Alien'
        special: 'Sprinter'
        for alien in self.fleet:
            if alien.rect.bottom >= self.settings.screen_h:
                alien.rect.y = 0
        for special in self.special:
            if special.rect.bottom >= self.settings.screen_h:
                special.rect.y - 0"""

    def check_fleet_bottom(self):

        """Checks if any aliens in either of the sprite groups are touching the bottom of the screen"""

        alien: 'Alien'
        for alien in self.fleet:
            if alien.rect.bottom >= self.settings.screen_h:
                alien.y = 0
        for alien in self.special:
            if alien.rect.bottom >= self.settings.screen_h:
                alien.y = 0
        
    
    def check_alien_count(self):

        """Checks if any aliens are in the Fleet sprite Group"""

        return not self.fleet
    
    def check_special_count(self):
        
        """Checks is any aliens are in the Special sprite group"""

        return not self.special

    
        


        
