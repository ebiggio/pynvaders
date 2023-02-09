import pygame
from alien import Alien


class Fleet:
    def __init__(self, pynvaders_game):
        """Initialize the fleet"""
        self.pynvaders_game = pynvaders_game
        self.screen = pynvaders_game.screen
        self.settings = pynvaders_game.settings
        self.stats = pynvaders_game.stats
        self.ship = pynvaders_game.ship
        # This will store all data related to the fleet (type, health, points, etc)
        self.fleet_data = None
        # Hold the rows of the fleet
        self.alien_rows = dict()
        # Contains the direction of the rows of the fleet: 1 represents right; -1 represents left
        self.row_direction = dict()

        self.alien_image = pygame.image.load('images/alien.bmp')

    def create_fleet(self):
        """Create the fleet of aliens"""
        # Create an alien and find the number of aliens in a row
        # Spacing between each alien is equal to one alien width
        alien = Alien(self.pynvaders_game, self.alien_image, 0, 0)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of aliens that fit on the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Create the full fleet of aliens
        self.fleet_data = dict()
        for row_number in range(number_rows):
            self.fleet_data[row_number] = dict()
            self.row_direction[row_number] = 1
            self.alien_rows[row_number] = pygame.sprite.Group()
            for alien_number in range(number_aliens_x):
                # This will store all data related to the alien (type, health, points, etc). For now, it's just a 1,
                # that represents the alien's HP
                self.fleet_data[row_number][alien_number] = 1
                self._create_alien(row_number, alien_number)

    def _create_alien(self, row_number, alien_number):
        """Create an alien and place it in the row"""
        alien = Alien(self.pynvaders_game, self.alien_image, row_number, alien_number)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.alien_rows[row_number].add(alien)

    def update_aliens(self):
        """Check if any of the rows of the fleet is at an edge, then update the position of all aliens in the row"""
        self._check_row_edges()

        # Look for alien-ship collisions
        for row, aliens in self.alien_rows.items():
            for alien in aliens:
                alien.update(self.row_direction[row])

                if alien.rect.colliderect(self.ship.rect):
                    self.pynvaders_game.ship_hit()

                    return

        # Look for aliens hitting the bottom of the screen
        self._check_bottom_screen()

    def _check_row_edges(self):
        """Respond appropriately if any aliens in a row have reached an edge"""
        for row, aliens in self.alien_rows.items():
            for alien in aliens:
                if alien.check_edges():
                    # For the first 5 levels, the aliens will be polite enough to wait for the rows in "front" of them
                    # to be destroyed before moving down
                    if self.stats.level in range(1, 6):
                        if not row + 1 in self.alien_rows:
                            self._drop_and_change_row_direction(row)
                        else:
                            self.row_direction[row] *= -1
                    else:
                        self._drop_and_change_row_direction(row)
                    break

    def _drop_and_change_row_direction(self, row_number):
        """Drop a row of the fleet and change its direction"""
        for alien in self.alien_rows[row_number]:
            alien.rect.y += self.settings.fleet_drop_speed
        self.row_direction[row_number] *= -1

    def _check_bottom_screen(self):
        """Check if any aliens have reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for row, aliens in self.alien_rows.items():
            for alien in aliens:
                if alien.rect.bottom >= screen_rect.bottom:
                    # Treat this the same as if the ship got hit
                    self.pynvaders_game.ship_hit()

                    return
