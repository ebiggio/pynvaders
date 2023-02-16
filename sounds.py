import pygame
import random


class Sounds:
    # Class to load and play the sounds of the game

    def __init__(self):
        # Ship (player) bullet sound
        # We create a channel for the bullet sound so that it doesn't overlap with the hit sound
        self.ship_bullet_channel = pygame.mixer.Channel(0)
        self.ship_bullet_channel.set_volume(0.3)
        self.ship_bullet_sound = pygame.mixer.Sound('sounds/ship_bullet.wav')

        # Hit sound
        # We create a channel for the hit sound so that it doesn't overlap with the bullet sound, and we set the volume
        # to 1 so that it's louder than the bullet sound
        self.hit_channel = pygame.mixer.Channel(1)
        self.hit_channel.set_volume(1)
        self.hit_sound = pygame.mixer.Sound('sounds/hit.wav')

        # Explosion sound
        # We create a channel for the explosion sound so that it doesn't overlap with the other sounds
        self.explosion_channel = pygame.mixer.Channel(2)
        self.explosion_channel.set_volume(0.5)
        self.explosion_sound1 = pygame.mixer.Sound('sounds/explosions/explosion_1.wav')
        self.explosion_sound2 = pygame.mixer.Sound('sounds/explosions/explosion_2.wav')

        # Alien bullet sound
        self.alien_bullet_channel = pygame.mixer.Channel(3)
        self.alien_bullet_channel.set_volume(0.5)
        self.alien_bullet_sound = pygame.mixer.Sound('sounds/alien_bullet.wav')

        # Alien kamikaze sound
        self.alien_kamikaze_channel = pygame.mixer.Channel(4)
        self.alien_kamikaze_channel.set_volume(1)
        self.alien_kamikaze_sound = pygame.mixer.Sound('sounds/alien_kamikaze.wav')

    def play_bullet_sound(self):
        # Plays the bullet sound
        self.ship_bullet_channel.play(self.ship_bullet_sound)

    def play_hit_sound(self):
        # Plays the hit sound
        self.hit_channel.play(self.hit_sound)

    def play_explosion_sound(self):
        # Plays a random explosion sound
        # We randomly choose one of the two explosion sounds
        explosion_sound = random.choice([self.explosion_sound1, self.explosion_sound2])
        # We play the explosion sound
        self.explosion_channel.play(explosion_sound)

    def play_alien_bullet_sound(self):
        # Plays the alien bullet sound
        self.alien_bullet_channel.play(self.alien_bullet_sound)

    def play_alien_kamikaze_sound(self):
        # Plays the alien kamikaze sound
        self.alien_kamikaze_channel.play(self.alien_kamikaze_sound)
