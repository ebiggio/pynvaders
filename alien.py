import random
import time

from pygame.sprite import Sprite
from bullets import AlienBullet


class Alien(Sprite):
    """A class to represent a single alien in the fleet"""

    def __init__(self, pynvaders_game, alien_class, hp, image, row_number, alien_number):
        """Initialize the alien and set its starting position"""
        super().__init__()
        self.screen = pynvaders_game.screen
        self.settings = pynvaders_game.settings
        self.stats = pynvaders_game.stats
        self.player_bullets = pynvaders_game.player_bullets
        self.alien_bullets = pynvaders_game.alien_bullets
        self.sounds = pynvaders_game.sounds

        # Store the alien's class and HP
        self.alien_class = alien_class
        self.hp = hp

        self.row_number = row_number
        self.alien_number = alien_number

        # Load the alien image and set its rect attribute
        self.image = image
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact horizontal position
        self.x = float(self.rect.x)

    def check_edges(self):
        """Returns True if alien is at edge of the screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self, row_number):
        """Move the alien right or left"""
        self.x += (self.settings.alien_speed * row_number)
        self.rect.x = self.x

        # After two seconds in the level, the aliens will start doing their special actions
        if time.time() - self.stats.start_time >= 2:
            if self.alien_class == 'orange':
                # Orange aliens will shoot bullets
                self._shoot_bullet()

    def _shoot_bullet(self):
        """Shoot a bullet from the alien"""
        if len(self.alien_bullets) < self.settings.alien_bullets_allowed:
            shooting_chance = random.choice(range(1, 100))

            # The chance of the alien shooting a bullet is 70%
            if shooting_chance <= 70:
                new_alien_bullet = AlienBullet(self, self.rect.midbottom)
                self.alien_bullets.add(new_alien_bullet)
                self.sounds.play_alien_bullet_sound()
