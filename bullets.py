import pygame
from pygame.sprite import Sprite


class BaseBullet(Sprite):
    """A class to manage the bullets from the game"""
    def __init__(self, pynvaders_game):
        super().__init__()
        self.screen = pynvaders_game.screen
        self.settings = pynvaders_game.settings
        self.player_bullets = pynvaders_game.player_bullets
        self.alien_bullets = pynvaders_game.alien_bullets

        self.color = None
        self.y = 0

        self.direction = 0
        self.speed = 0

    def update(self):
        """Move the bullet up or down the screen"""
        # Update the decimal position of the bullet
        self.y += self.speed * self.direction
        # Update the rect position
        self.rect.y = self.y

        if self.direction == -1 and self.rect.bottom <= 0:
            # When a ship's bullet moves off the top of the screen, remove it from the bullets group
            self.player_bullets.remove(self)
        elif self.direction == 1 and self.rect.top >= self.screen.get_rect().bottom:
            # When an alien's bullet moves off the bottom of the screen, remove it from the bullets group
            self.alien_bullets.remove(self)

    def draw_bullet(self):
        """Draw the bullet to the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)


class PlayerBullet(BaseBullet):
    """A class to manage bullets fired from the ship"""
    def __init__(self, pynvaders_game):
        super().__init__(pynvaders_game)
        self.color = self.settings.player_bullet_color

        # The ship's bullets move up the screen
        self.direction = -1
        self.speed = self.settings.player_bullet_speed

        # Create a bullet rect at (0, 0)
        self.rect = pygame.Rect(0, 0, self.settings.player_bullet_width, self.settings.player_bullet_height)

        # Set the bullet's starting position at the ship's position
        self.rect.midtop = pynvaders_game.ship.rect.midtop

        # Store the bullet's position as a decimal value
        self.y = float(self.rect.y)


class AlienBullet(BaseBullet):
    """A class to manage bullets fired from the aliens"""
    def __init__(self, pynvaders_game, alien_rect_midbottom):
        super().__init__(pynvaders_game)
        self.color = self.settings.alien_bullet_color

        # The alien's bullets move down the screen
        self.direction = 1
        self.speed = self.settings.alien_bullet_speed

        # Create a bullet rect at (0, 0)
        self.rect = pygame.Rect(0, 0, self.settings.alien_bullet_width, self.settings.alien_bullet_height)

        # Set the bullet's starting position at the alien's position
        self.rect.midtop = alien_rect_midbottom

        # Store the bullet's position as a decimal value
        self.y = float(self.rect.y)
