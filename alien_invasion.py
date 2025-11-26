import sys
import pygame
from settings import Settings
from ship import Ship
from arsenal import Arsenal
from alien_fleet import AlienFleet
from game_stats import GameStats
from time import sleep
from button import Button
from hud import HUD

class AlienInvasion:

    """This class is the main game loop"""

    def __init__(self):

        """
        Initializes all of the main game stats and settings
        Establishes the sound settings
        Causes other classes to initialize
        """

        #Establishes the main settings
        pygame.init()
        self.settings = Settings()
        self.settings.initialize_dynamic_settings()
        
        #Sets up the basic screen and background
        self.screen = pygame.display.set_mode((self.settings.screen_w, self.settings.screen_h))
        pygame.display.set_caption(self.settings.name)

        self.bg = pygame.image.load(self.settings.bg_file)
        self.bg = pygame.transform.scale(self.bg, (self.settings.screen_w, self.settings.screen_h))

        #Establishes the game clock
        self.running = True
        self.clock = pygame.time.Clock()

        #Sets up all sound settings
        pygame.mixer.init()
        self.lazer_sound = pygame.mixer.Sound(self.settings.lazer_sound)
        self.lazer_sound.set_volume(0.25)
        self.impact = pygame.mixer.Sound(self.settings.impact_sound)
        self.impact.set_volume(1)
        
        #Initilizes the HUD and Game Stats
        self.game_stats = GameStats(self)
        self.HUD = HUD(self)

        #Initializes the ship, fleet, and button
        self.ship = Ship(self, Arsenal(self))
        self.alien_fleet = AlienFleet(self)
        self.play_button = Button(self, "Play")
        self.game_active = False

    def run_game(self):
        
        """
        The Main Game Loop 
        Runs in three sections:
        Check events
        Update and check collisions
        Update the screen
        """

        while self.running:
            self._check_events()

        #While playing game loop
            if self.game_active:
                self.ship.update()
                self.alien_fleet.update_fleet()
                self._check_colissions()            

            self._update_screen() 
            self.clock.tick(self.settings.FPS)

    def _check_colissions(self):

        """
        Checks many collsions:
        Ship to aliens - loose a life
        cannon to alien - kill alien
        round to alien - delete both
        Check if aliens are gone - increment level
        """

        #check collisions for ship
        if self.ship.check_collisions(self.alien_fleet.fleet) or self.ship.check_collisions(self.alien_fleet.special):
            self.check_game_status()

        #check collisions for aliens and screen bottom
        self.alien_fleet.check_fleet_bottom()
        
        #check collisions for bullets and aliens
        self.basic_cannon_collision()
        self.special_cannon_collision()
        
        #check collisions for rounds and aliens
        self.basic_round_collision()
        self.special_round_collision()

        #check if aliens are gone
        if self.alien_fleet.check_alien_count() and self.alien_fleet.check_special_count():
            self._reset_level()
            self.settings.increase_difficulty()
            #upgrade game stats level
            self.game_stats.update_level()
            self.HUD.update_level()
            #update game hud veiw

        pass

    def special_round_collision(self):

        """Checks Collision for secondary gun shots and the special alien fleet"""

        collisions_cannon1 = self.alien_fleet.check_special_round_collisions(self.ship.arsenal.cannon1)
        collisions_cannon2 = self.alien_fleet.check_special_round_collisions(self.ship.arsenal.cannon2)
        if collisions_cannon1:
            self.game_stats.update(collisions_cannon1, self.settings.sprinter_points)
            self.impact.play()
            self.impact.fadeout(150)
            self.HUD.update_scores()
        if collisions_cannon2:
            self.game_stats.update(collisions_cannon2, self.settings.sprinter_points)
            self.impact.play()
            self.impact.fadeout(150)
            self.HUD.update_scores()

    def basic_round_collision(self):

        """Checks Collision for secondary gun shots and the alien fleet"""

        collisions_cannon1 = self.alien_fleet.check_round_collisions(self.ship.arsenal.cannon1)
        collisions_cannon2 = self.alien_fleet.check_round_collisions(self.ship.arsenal.cannon2)
        
        if collisions_cannon1:
            self.game_stats.update(collisions_cannon1, self.settings.alien_points)
            self.impact.play()
            self.impact.fadeout(150)
            self.HUD.update_scores()
        if collisions_cannon2:
            self.game_stats.update(collisions_cannon2, self.settings.alien_points)
            self.impact.play()
            self.impact.fadeout(150)
            self.HUD.update_scores()

    def special_cannon_collision(self):

        """Checks Collision for main gun shots and the special alien fleet"""

        collisions = self.alien_fleet.check_special_cannon_collisions(self.ship.arsenal.main_gun)
        if collisions:
            self.game_stats.update(collisions, self.settings.sprinter_points)
            self.HUD.update_scores()
            self.impact.play()
            self.impact.fadeout(150)

    def basic_cannon_collision(self):

        """Checks Collision for main gun shots and the alien fleet"""

        collisions = self.alien_fleet.check_cannon_collisions(self.ship.arsenal.main_gun)       
        if collisions:
            self.game_stats.update(collisions, self.settings.alien_points)
            self.HUD.update_scores()
            self.impact.play()
            self.impact.fadeout(150)

    def check_game_status(self):

        """Resets the level on death and checks the numbert of lives remaining"""

        if self.game_stats.ships_left > 0:
            self.game_stats.ships_left -= 1
            self._reset_level()
            sleep(0.5)
        else:
            self.game_active = False
      

    def _reset_level(self):

        """Resets the current level by emptying all sprite groups and reseting the aliens"""

        self.ship.arsenal.main_gun.empty()
        self.ship.arsenal.cannon1.empty()
        self.ship.arsenal.cannon2.empty()
        self.alien_fleet.fleet.empty()
        self.alien_fleet.special.empty()
        self.alien_fleet.create_fleet()

        pass

    def restart_game(self):

        """Resets the game stats for a new round"""

        #reset game stats
        self.game_stats.reset_stats()
        #reset screen and hub
        self.HUD.update_scores()
        self.settings.initialize_dynamic_settings()
        self._reset_level
        self.ship._center_ship
        self.game_active = True
        pygame.mouse.set_visible = False

    def _update_screen(self):

        """Updates and flips the screen"""

        self.screen.blit(self.bg, (0,0))
        self.ship.draw()
        self.alien_fleet.draw_fleet()
        self.HUD.draw()

        #Different Update when the game is not active
        if not self.game_active:
            self.play_button.draw()
            pygame.mouse.set_visible = True

        pygame.display.flip()



    def _check_events(self):

        """Checks Events like keydown and keyup"""

        for event in pygame.event.get():
            #Quit Function
            if event.type == pygame.QUIT:
                self.running = False
                self.game_stats.save_scores()
                pygame.quit()
                sys.exit()
            #KeyDown events
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            #KeyUp events
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            #Mouse Click
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_button_clicked()

    def _check_button_clicked(self):

        """Checks where the mouse is clicking"""

        mouse_pos = pygame.mouse.get_pos()
        if self.play_button.check_clicked(mouse_pos):
            self.restart_game()


    def _check_keydown_events(self, event):

        """Checks for all keydown events"""

        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_1:
            if self.ship.fire_main_gun():
                self.lazer_sound.play()
        elif event.key == pygame.K_2:
            if self.ship.fire_cannon1():
                self.lazer_sound.play()
        elif event.key == pygame.K_3:
            if self.ship.fire_cannon2():
                self.lazer_sound.play()
        elif event.key == pygame.K_q:
            self.running = False
            self.game_stats.save_scores()
            pygame.quit()
            sys.exit()
    
    def _check_keyup_events(self, event):

        """Checks for all keyup events"""

        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()

