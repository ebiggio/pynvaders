import pygame
from alien import Alien


class Fleet:
    def __init__(self, pynvaders_game):
        """Initialize the fleet"""
        self.pynvaders_game = pynvaders_game
        self.fleet_rows = None
        self.screen = pynvaders_game.screen
        self.settings = pynvaders_game.settings
        self.aliens = pygame.sprite.Group()
        self.ship = pynvaders_game.ship

    def create_fleet(self):
        """Create the fleet of aliens"""
        # Create an alien and find the number of aliens in a row
        # Spacing between each alien is equal to one alien width
        alien = Alien(self.pynvaders_game, 0, 0)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of aliens that fit on the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Create the full fleet of aliens
        self.fleet_rows = dict()
        for row_number in range(number_rows):
            self.fleet_rows[row_number] = dict()
            for alien_number in range(number_aliens_x):
                # This will store all data related to the alien (type, health, points, etc). For now, it's just a 1,
                # that represents the alien's HP
                self.fleet_rows[row_number][alien_number] = 1
                self._create_alien(row_number, alien_number)

    def _create_alien(self, row_number, alien_number):
        """Create an alien and place it in the row"""
        alien = Alien(self.pynvaders_game, row_number, alien_number)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def change_fleet_direction(self):
        """Drop the entire fleet and change its direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break

    def update_aliens(self):
        """Check if the fleet is at an edge, then update the position of all aliens in the fleet"""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self.pynvaders_game.ship_hit()

        # Look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit
                self.pynvaders_game.ship_hit()
                break
