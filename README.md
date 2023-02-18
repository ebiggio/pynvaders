# Pynvaders

A simple space invaders clone written in Python using Pygame, made from the "**Python Crash Course**" (2nd edition) book.

Tag `v1.0.0` is the final version of the game as it is in the book (with some mistakes from my part). From that point forward, all changes are my own experiments, features and improvements.

To run the game, install the dependencies and run the `pynvaders.py` file.

`python -m pip install --user pygame`

## Controls

- Use the arrow keys to move the ship left and right
- Press the spacebar to fire bullets
- Press the `q` key to quit the game

## Features

- Each row of aliens can move independently of the others (in the original game, all rows move together)
- In the first 5 levels, only the row of aliens closest to the ship will move down
- For the first 2 levels, only the green aliens will be present (the base alien)
- For levels 3-5, there will be a 15% chance of a blue alien replacing a green alien
  - Blue aliens in the last 3 rows have a chance to do a kamikaze attack (they move directly towards the bottom of the screen)
- For level 6 and forward, blue and orange aliens will have a chance to appear
  - Orange aliens have a chance to shoot a bullet
- For the fourth level and forward, all classes of aliens will have a chance to have more HP
  - Each alien class have 3 possible HP values:
    - Green: 1, 3 and 4
    - Blue: 3, 5 and 7
    - Orange: 1, 2 and 3
  - An alien with a higher HP value will have a different, more "colored" sprite than the base class sprite. Upon getting hit, the sprite will change to a more "pale" version of the same color (to represent the alien's current HP value), and a hit sound will be played (instead of the explosion sound that plays when an alien is destroyed)

## Credits

- [**Python Crash Course**](https://nostarch.com/pythoncrashcourse2e) by Eric Matthes (2nd edition)
- [**Alien ship images**](https://carlosalface.blogspot.com/2019/04/naves-espaciais-2d-pack-16.html) by Carlos Alface