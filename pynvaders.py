import sys
from time import sleep
import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from button import Button
from scoreboard import Scoreboard
from fleet import Fleet


class Pynvaders:
    """Main class for the game"""

    def __init__(self):
        """Initialize the game and create game resources"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Pynvaders")

        # Create an instance to store game statistics and create a scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

        # Create the fleet of aliens
        self.fleet = Fleet(self)

        # Make the play button
        self.play_button = Button(self, "Play")

        # Load the bullet sound
        self.bullet_sound = pygame.mixer.Sound('sounds/bullet.wav')

    def run_game(self):
        """Main loop for the game"""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self.bullets.update()
                self._update_bullets()
                self.fleet.update_aliens()

            self._update_screen()

    def _check_events(self):
        """Respond to key presses and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks the 'Play' button"""
        if self.play_button.rect.collidepoint(mouse_pos) and not self.stats.game_active:
            # Reset the game settings
            self.settings.initialize_dynamic_settings()

            # Reset the game statistics
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ship()

            # Get rid of any remaining aliens and bullets
            self.fleet.alien_rows = dict()
            self.bullets.empty()

            # Create a new fleet and center the ship
            self.fleet.create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Respond to key presses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE and self.stats.game_active:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """Respond to key releases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.bullet_sound.play()

    def _update_bullets(self):
        """Update positions of bullets and get rid of old bullets"""
        # Update bullet positions
        self.bullets.update()

        # Get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions"""
        # Remove any bullets and aliens that have collided
        for row, aliens in self.fleet.alien_rows.copy().items():
            collisions = pygame.sprite.groupcollide(self.bullets, aliens, True, False)

            if collisions:
                for aliens_hit in collisions.values():
                    for alien in aliens_hit:
                        self.fleet.fleet_data[alien.row_number][alien.alien_number] -= 1
                        # We check the alien's health to see if it's dead
                        if self.fleet.fleet_data[alien.row_number][alien.alien_number] <= 0:
                            aliens.remove(alien)
                            self.stats.score += self.settings.alien_points * len(aliens_hit)

                if len(aliens) == 0:
                    self.fleet.alien_rows.pop(row)

            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.fleet.alien_rows:
            # Destroy existing bullets and create new fleet
            self.bullets.empty()
            self.fleet.create_fleet()
            self.settings.increase_speed()

            # Increase level
            self.stats.level += 1
            self.sb.prep_level()

    def ship_hit(self):
        """Respond to the ship being hit by an alien"""
        if self.stats.ships_left > 0:
            # Decrement ships_left, and update scoreboard
            self.stats.ships_left -= 1
            self.sb.prep_ship()

            # Get rid of any remaining aliens and bullets
            self.fleet.alien_rows = dict()
            self.bullets.empty()

            # Create a new fleet and center the ship
            self.fleet.create_fleet()
            self.ship.center_ship()

            # Pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        for row, aliens in self.fleet.alien_rows.items():
            aliens.draw(self.screen)

        # Draw the score information
        self.sb.show_score()

        # Draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible
        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game
    pynvaders = Pynvaders()
    pynvaders.run_game()
