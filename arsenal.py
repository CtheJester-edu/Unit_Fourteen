import pygame
from typing import TYPE_CHECKING
from bullet import Bullet
from round_1 import Round1
from round_2 import Round2

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    

class Arsenal:

    """Manages all of the weapons and their shots"""

    def __init__(self, game:'AlienInvasion'):

        """Initializes the settings and sprite groups"""

        self.game = game
        self.settings = game.settings
        self.main_gun = pygame.sprite.Group()
        self.cannon1 = pygame.sprite.Group()
        self.cannon2 = pygame.sprite.Group()

    def update_arsenal(self):

        """Updates all shots and checks if they are offscreen"""

        self.main_gun.update()
        self._remove_bullets_offscreen()

        self.cannon1.update()
        self.cannon2.update()
        self._remove_round1_offscreen()
        self._remove_round2_offscreen()

    def _remove_bullets_offscreen(self):

        """Checks if any bullets are offscreen and removes them if necessary"""

        for bullet in self.main_gun.copy():
            if bullet.rect.bottom <= 0:
                self.main_gun.remove(bullet)

    def _remove_round1_offscreen(self):

        """Checks if any rounds in group 1 are offscreen and removes them if necessary"""

        for round in self.cannon1.copy():
            if round.rect.bottom <= 0:
                self.cannon1.remove(round)

    def _remove_round2_offscreen(self):

        """Checks if any rounds in group 2 are offscreen and removes them if necessary"""

        for round in self.cannon2.copy():
            if round.rect.bottom <= 0:
                self.cannon2.remove(round)

    def draw(self):
        
        """Draws all shots"""
        
        for bullet in self.main_gun:
            bullet.draw_bullet()
        
        for round in self.cannon1:
            round.draw_round()

        for round in self.cannon2:
            round.draw_round()

    def fire_bullet(self):

        """Fires and new bullet from the main cannon"""

        if len(self.main_gun) < self.settings.bullet_amount:
            new_bullet = Bullet(self.game)
            self.main_gun.add(new_bullet)
            return True
        return False

    def fire_round1(self):

        """Fires a round from gun 1"""

        if len(self.cannon1) < self.settings.round_amount:
            new_round = Round1(self.game)
            self.cannon1.add(new_round)
            return True
        return False
    
    def fire_round2(self):

        """Fires a round from gun 2"""
        
        if len(self.cannon2) < self.settings.round_amount:
            new_round = Round2(self.game)
            self.cannon2.add(new_round)
            return True
        return False