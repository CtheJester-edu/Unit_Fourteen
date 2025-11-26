import pygame
from typing import TYPE_CHECKING
from pathlib import Path
import json

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class GameStats():

    def __init__(self, game: 'AlienInvasion'):
        self.game = game
        self.settings = game.settings
        self.max_score = 0
        self.reset_stats()
        self.init_saved_scores()

    def init_saved_scores(self):
        self.path = self.settings.scores_file
        if self.path.exists():
            contents = self.path.read_text()
            scores = json.loads(contents)
            self.hi_score = scores.get('hi_score', 0)
        else:
            self.hi_score = 0
            self.save_scores()


    def reset_stats(self):
        self.ships_left = self.settings.ship_lives
        self.score = 0
        self.level = 1

    def update(self, collisions, target_type):
        #update score
        self._update_score(collisions, target_type)
        #update maxscore
        self._update_max_score()
        #update highscore
        self._update_hi_score()

    def _update_max_score(self):
        if self.score > self.max_score:
            self.max_score = self.score
            #print(f'{self.max_score}')
        

    def _update_score(self, collisions, target_type):
        for alien in collisions.values():
            self.score += target_type
            #print(f'{self.score}')

    def _update_hi_score(self):
        if self.max_score > self.hi_score:
            self.hi_score = self.max_score
            #print(f'high score = {self.hi_score}')

    def update_level(self):
        self.level += 1

    def save_scores(self):
        scores = {'hi_score' : self.hi_score}
        contents = json.dumps(scores, indent=4)
        try:
            self.path.write_text(contents)
        except FileNotFoundError as e:
            print(F'File Not Found: {e}')

    

