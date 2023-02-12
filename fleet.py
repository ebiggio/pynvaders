import pygame
import os
import random
from alien import Alien


class Fleet:
    def __init__(self, pynvaders_game):
        """Initialize the fleet"""
        self.pynvaders_game = pynvaders_game
        self.screen = pynvaders_game.screen
        self.settings = pynvaders_game.settings
        self.stats = pynvaders_game.stats
        self.ship = pynvaders_game.ship
        # Holds the rows of the fleet
        self.alien_rows = dict()
        # Contains the direction of the rows of the fleet: 1 represents right; -1 represents left
        self.row_direction = dict()
        # Holds the 3 types of images for the different classes of aliens
        self.alien_images = dict()
        self._load_alien_images()

        # Holds the base HP of each alien class
        self.alien_classes_hp = {
            'green': [1, 3, 4],
            'blue': [3, 5, 7],
            'orange': [1, 2, 3],
        }

    def _load_alien_images(self):
        """Load the alien images, and store them in a dictionary"""
        """
        The dictionary will be structured as follows:
            alien_images = {
                'blue': {
                    1: <image>,
                    2: <image>,
                    3: <image>,
                },
                'green': {
                    1: <image>,
                    2: <image>,
                    3: <image>,
                },
                'orange': {
                    etc...
        """
        for path, subdir, filenames in os.walk('images/aliens/'):
            for name in filenames:
                if name.endswith('.png'):
                    filename = name[:-4]
                    directory_name = os.path.basename(path)

                    if directory_name not in self.alien_images:
                        self.alien_images.update({directory_name: dict()})

                    img = pygame.image.load(os.path.join(path, name)).convert_alpha()
                    self.alien_images[directory_name].update({int(filename): img})

    def create_fleet(self):
        """Create the fleet of aliens"""
        # Create an alien and find the number of aliens in a row
        # Spacing between each alien is equal to one alien width
        alien = Alien(self.pynvaders_game, 'green', 1, self.alien_images['green'][1], 0, 0)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of aliens that fit on the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Create the full fleet of aliens
        for row_number in range(number_rows):
            self.row_direction[row_number] = 1
            self.alien_rows[row_number] = pygame.sprite.Group()
            for alien_number in range(number_aliens_x):
                alien_data = self._get_alien_class_and_hp()
                image_index = self.alien_classes_hp[alien_data[0]].index(alien_data[1]) + 1

                self._create_alien(alien_data[0], alien_data[1], image_index, row_number, alien_number)

    def _create_alien(self, alien_class, hp, image_index, row_number, alien_number):
        """Create an alien and place it in the row"""
        alien = Alien(self.pynvaders_game, alien_class, hp, self.alien_images[alien_class][image_index]
                      , row_number, alien_number)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.alien_rows[row_number].add(alien)

    def _get_alien_class_and_hp(self):
        """Get a random alien class and HP"""
        # For the first 2 levels, only the green aliens will be present
        if self.stats.level in range(1, 3):
            possible_classes = ['green']
            possible_classes_prob = [1]
        elif self.stats.level in range(3, 6):
            # For levels 3-5, there will be a 15% chance of the blue aliens being present
            possible_classes = ['green', 'blue']
            possible_classes_prob = [0.85, 0.15]
        else:
            # From level 6 and forward, we will calculate the probability of each alien class being chosen, increasing
            # as the player progresses through the levels
            possible_classes = ['green', 'blue', 'orange']
            green_prob = (self.stats.level - 5) * 0.01
            blue_prob = (self.stats.level - 5) * 0.001
            orange_prob = (self.stats.level - 5) * 0.0005
            possible_classes_prob = [green_prob, blue_prob, orange_prob]

        alien_class_list = random.choices(possible_classes, weights=possible_classes_prob)
        alien_class = alien_class_list[0]

        # From the fourth level and forward, there will be a small probability for the chosen alien class to have more
        # HP. Each alien class have 3 possible HP values, and the probability of each one is 85%, 10% and 5%
        if self.stats.level > 4:
            alien_hp = random.choices(self.alien_classes_hp[alien_class], weights=[0.85, 0.10, 0.05])
        else:
            alien_hp = self.alien_classes_hp[alien_class]

        return alien_class, alien_hp[0]

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
