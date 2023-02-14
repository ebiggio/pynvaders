class Settings:
    """A class to store all settings for Pynvaders"""

    def __init__(self):
        """Initialize the game's settings"""
        # Screen settings
        self.screen_width = 1300
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Ship settings
        self.ship_speed = 1.5
        self.ship_limit = 3

        # Player bullet settings
        self.player_bullet_speed = 1.0
        self.player_bullet_width = 3
        self.player_bullet_height = 15
        self.player_bullet_color = (60, 60, 60)
        self.player_bullets_allowed = 3

        # Alien bullet settings
        self.alien_bullet_speed = 0.3
        self.alien_bullet_width = 4
        self.alien_bullet_height = 20
        self.alien_bullet_color = 'darkorange'
        self.alien_bullets_allowed = 4

        # Alien settings
        self.alien_speed = 0.2
        self.fleet_drop_speed = 10

        # How quickly the game speeds up
        self.speedup_scale = 1.1

        # How quickly the alien point value increases
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game"""
        self.ship_speed = 1.5
        self.player_bullet_speed = 1.0
        self.alien_speed = 0.2

        # Scoring
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings"""
        self.player_bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
