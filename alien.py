import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """A class to represent a single alien in the fleet"""

    def __init__(self, pynvaders_game, alien_image, row_number, alien_number):
        """Initialize the alien and set its starting position"""
        super().__init__()
        self.screen = pynvaders_game.screen
        self.settings = pynvaders_game.settings

        self.row_number = row_number
        self.alien_number = alien_number

        # Load the alien image and set its rect attribute
        self.image = alien_image
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
