from pathlib import Path

class Settings:
    
    def __init__(self):

        """
        Establishes the main game settings. 
        Comments separating each block of variables tells you what the section does.
        """

        #Basic Game Settings
        self.name: str = "Alien Invasion"
        self.screen_w = 1200
        self.screen_h = 800
        self.FPS = 60
        self.bg_file = Path.cwd() / 'Assets' / 'images' / 'Starbasesnow.png'
        self.difficulty_scale = 1.1
        self.scores_file = Path.cwd() / 'Assets' / 'file' / 'scores.json'

        #Ship Settings
        self.ship_file = Path.cwd() / 'Assets' / 'images' / 'ship2(no bg).png'
        self.ship_w = 40
        self.ship_h = 60
        
        #Settings for Main Gun
        self.bullet_file = Path.cwd() / 'Assets' / 'images' / 'laserBlast.png'
        self.lazer_sound = Path.cwd() / 'Assets' / 'sound' / 'laser.mp3'
        self.bullet_speed = 7
        self.bullet_w = 25
        self.bullet_h = 80

        #Settings for Cannons
        self.round_file = Path.cwd() / 'Assets' / 'images' / 'laserBlast.png'
        self.round_speed = 7
        self.round_w = 12.5
        self.round_h = 40      
        
        #Alien Settings
        self.alien_file = Path.cwd() / 'Assets' / 'images' / 'enemy_4.png'
        self.alien_w = 80
        self.alien_h = 80

        #Sprinter File
        self.sprinter_file = Path.cwd() / 'Assets' / 'images' / 'Asteroid Brown.png'

        #Fleet Settings
        self.impact_sound = Path.cwd() / 'Assets' / 'sound' / 'impactSound.mp3'
        self.fleet_hit_bottom = False

        #Button Settings
        self.button_w = 200
        self.button_h = 50
        self.button_color = (0,135,50)
        self.button_font_size = 48

        #Hud Settings
        self.text_color = (255,255,255)
        self.HUD_font_size = 20

        #Font File Access
        self.font_file = Path.cwd() / 'Assets' / 'Fonts' / 'Silkscreen' / 'Silkscreen-Bold.ttf'

    def initialize_dynamic_settings(self):

        """
        Initializes all changing settings and resets them as needed
        Divided as above by inline comments
        """

        #Ship Settings
        self.ship_speed = 5
        self.ship_lives = 3
        
        #Weapon Settings
        self.bullet_amount = 5
        self.round_amount = 5
        
        #Fleet Settings
        self.fleet_speed = 5
        self.fleet_direction = 1
        self.fleet_drop_speed = 40
        self.sprinter_speed = 5

        #Score Settings
        self.alien_points = 50
        self.sprinter_points = 75
        self.round_score = 10

    def increase_difficulty(self):

        """Increases different stats to scale the difficulty"""

        self.ship_speed *= self.difficulty_scale
        self.bullet_speed *= self.difficulty_scale
        self.fleet_speed *= self.difficulty_scale
        self.alien_points *= self.difficulty_scale
        self.sprinter_points *= self.difficulty_scale
        self.round_score *= self.difficulty_scale

