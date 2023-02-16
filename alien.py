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

        # Store the alien's exact horizontal and vertical position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # Alien ability cooldown
        self.ability_cooldown = time.time()

        # Kamikaze attack. If active, the alien will move directly towards the bottom of the screen
        self.kamikaze = False

    def check_edges(self):
        """Returns True if alien is at edge of the screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self, row_direction):
        """Move the alien right or left, unless it's in kamikaze mode. In that case, it will move down"""
        if self.kamikaze:
            self.y += self.settings.alien_speed
            self.rect.y = self.y
        else:
            self.x += (self.settings.alien_speed * row_direction)
            self.rect.x = self.x

        # After two seconds in the level, the aliens will start doing their special actions
        if time.time() - self.stats.start_time >= 2:
            if self.alien_class == 'orange':
                # Orange aliens will shoot bullets
                self._shoot_bullet()
            elif self.alien_class == 'blue':
                # Blue aliens will activate kamikaze
                self._activate_kamikaze()

    def _shoot_bullet(self):
        """Shoot a bullet from the alien"""
        # A single orange alien will only have a chance of shooting a bullet every 2 seconds
        if len(self.alien_bullets) < self.settings.alien_bullets_allowed and time.time() - self.ability_cooldown >= 2:
            # The chance of the alien shooting a bullet is 80%
            if random.choice(range(1, 100)) <= 80:
                new_alien_bullet = AlienBullet(self, self.rect.midbottom)
                self.alien_bullets.add(new_alien_bullet)
                self.sounds.play_alien_bullet_sound()

            self.ability_cooldown = time.time()

    def _activate_kamikaze(self):
        """Try to activate kamikaze attack for the blue aliens that are in the back 3 rows, but only every 2 second"""
        if not self.kamikaze and self.row_number <= 2 <= time.time() - self.ability_cooldown:
            # The chance of the alien activating kamikaze is 50%
            if random.choice(range(1, 100)) <= 50:
                self.kamikaze = True
                self.sounds.play_alien_kamikaze_sound()

            self.ability_cooldown = time.time()
