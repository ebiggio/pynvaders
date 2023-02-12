import pygame
import random


class Sounds:
    # Class to load and play the sounds of the game

    def __init__(self):
        # Bullet sound
        # We create a channel for the bullet sound so that it doesn't overlap with the hit sound
        self.bullet_channel = pygame.mixer.Channel(0)
        self.bullet_channel.set_volume(0.3)
        self.bullet_sound = pygame.mixer.Sound('sounds/bullet.wav')

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

    def play_bullet_sound(self):
        # Plays the bullet sound
        self.bullet_channel.play(self.bullet_sound)

    def play_hit_sound(self):
        # Plays the hit sound
        self.hit_channel.play(self.hit_sound)

    def play_explosion_sound(self):
        # Plays a random explosion sound
        # We randomly choose one of the two explosion sounds
        explosion_sound = random.choice([self.explosion_sound1, self.explosion_sound2])
        # We play the explosion sound
        self.explosion_channel.play(explosion_sound)
