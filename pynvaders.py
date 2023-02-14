import sys
import time
from time import sleep
import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
import bullets
from button import Button
from scoreboard import Scoreboard
from fleet import Fleet
from sounds import Sounds


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
        self.player_bullets = pygame.sprite.Group()
        self.alien_bullets = pygame.sprite.Group()

        # We load the sound library
        self.sounds = Sounds()

        # Create the fleet of aliens
        self.fleet = Fleet(self)

        # Make the play button
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Main loop for the game"""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
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
            self.sb.prep_ship()

            self.ship.center_ship()

            self._prepare_level()

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
        if len(self.player_bullets) < self.settings.player_bullets_allowed:
            new_player_bullet = bullets.PlayerBullet(self)
            self.player_bullets.add(new_player_bullet)
            self.sounds.play_bullet_sound()

    def _update_bullets(self):
        """Update positions of bullets and get rid of old bullets"""
        # Update bullet positions
        self.player_bullets.update()
        self.alien_bullets.update()

        self._check_bullet_alien_collisions()
        self._check_bullet_ship_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions"""
        for row, aliens in self.fleet.alien_rows.copy().items():
            # We remove any bullet that has collided with an alien
            collisions = pygame.sprite.groupcollide(self.player_bullets, aliens, True, False)

            if collisions:
                self.fleet.process_bullet_alien_collisions(collisions, aliens, row)

            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.fleet.alien_rows:
            # Increase level
            self.stats.level += 1

            # Increase game speed
            self.settings.increase_speed()

            self._prepare_level()

    def _check_bullet_ship_collisions(self):
        """Respond to bullet-ship collisions"""
        if pygame.sprite.spritecollideany(self.ship, self.alien_bullets):
            self.ship_hit()

    def ship_hit(self):
        """Respond to the ship being hit by an alien or an alien bullet"""
        if self.stats.ships_left > 0:
            # Decrement ships_left, and update scoreboard
            self.stats.ships_left -= 1
            self.sb.prep_ship()

            self.ship.center_ship()

            # Pause
            sleep(0.5)

            self._prepare_level()
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.player_bullets.sprites():
            bullet.draw_bullet()

        for bullet in self.alien_bullets.sprites():
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

    def _prepare_level(self):
        """Prepare the level's score"""
        self.sb.prep_level()

        # Destroy existing bullets and create new fleet
        self.player_bullets.empty()
        self.alien_bullets.empty()
        self.fleet.create_fleet()

        # Define the start time of the level
        self.stats.start_time = time.time()


if __name__ == '__main__':
    # Make a game instance, and run the game
    pynvaders = Pynvaders()
    pynvaders.run_game()
