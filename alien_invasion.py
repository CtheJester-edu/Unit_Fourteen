import sys
import pygame
from settings import Settings
from ship import Ship
from arsenal import Arsenal
#from alien import Alien
from alien_fleet import AlienFleet
from game_stats import GameStats
from time import sleep
from button import Button
from hud import HUD

class AlienInvasion:

    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.settings.initialize_dynamic_settings()
        

        self.screen = pygame.display.set_mode((self.settings.screen_w, self.settings.screen_h))
        pygame.display.set_caption(self.settings.name)

        self.bg = pygame.image.load(self.settings.bg_file)
        self.bg = pygame.transform.scale(self.bg, (self.settings.screen_w, self.settings.screen_h))

        self.running = True
        self.clock = pygame.time.Clock()

        pygame.mixer.init()
        self.lazer_sound = pygame.mixer.Sound(self.settings.lazer_sound)
        self.lazer_sound.set_volume(0.25)
        self.impact = pygame.mixer.Sound(self.settings.impact_sound)
        self.impact.set_volume(1)
        
        self.game_stats = GameStats(self)
        self.HUD = HUD(self)

        self.ship = Ship(self, Arsenal(self))
        self.alien_fleet =AlienFleet(self)
        #self.alien_fleet.create_fleet()
        self.play_button = Button(self, "Play")
        self.game_active = False

    def run_game(self):
        # Game Loop etc.
        while self.running:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self.alien_fleet.update_fleet()

                self._check_colissions()

            

            self._update_screen() 
            self.clock.tick(self.settings.FPS)

    def _check_colissions(self):

        #check collisions for ship
        if self.ship.check_collisions(self.alien_fleet.fleet):
            #alien fleet reset, player reset, loose one life.
            self.check_game_status()

        #check collisions for aliens and screen bottom
        if self.alien_fleet.check_fleet_bottom():
            self.check_game_status()
        
        

        #check collisions for bullets and aliens
        collisions = self.alien_fleet.check_collisions(self.ship.arsenal.arsenal)
        if collisions:
            self.game_stats.update(collisions)
            self.HUD.update_scores()
            self.impact.play()
            self.impact.fadeout(150)
        
        #check if aliens are gone
        if self.alien_fleet.check_alien_count():
            self._reset_level()
            self.settings.increase_difficulty()
            #upgrade game stats level
            self.game_stats.update_level()
            self.HUD.update_level()
            #update game hud veiw

        pass

    def check_game_status(self):
        if self.game_stats.ships_left > 0:
            self.game_stats.ships_left -= 1
            self._reset_level()
            sleep(0.5)
        else:
            self.game_active = False
      

    def _reset_level(self):
        self.ship.arsenal.arsenal.empty()
        self.alien_fleet.fleet.empty()
        self.alien_fleet.create_fleet()

        pass

    def restart_game(self):
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
        self.screen.blit(self.bg, (0,0))
        self.ship.draw()
        #self.alien.draw_alien()
        self.alien_fleet.draw_fleet()
        self.HUD.draw()
        #draw HUD

        if not self.game_active:
            self.play_button.draw()
            pygame.mouse.set_visible = True

        pygame.display.flip()



    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.game_stats.save_scores()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_button_clicked()

    def _check_button_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.play_button.check_clicked(mouse_pos):
            self.restart_game()


    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            if self.game_active == True:
                if self.ship.fire():
                    self.lazer_sound.play()
            #play the lazer sound
        elif event.key == pygame.K_q:
            self.running = False
            self.game_stats.save_scores()
            pygame.quit()
            sys.exit()
    
    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()

