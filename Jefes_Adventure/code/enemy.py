import pygame as pg
from tiles import AnimatedTile


class Enemy(AnimatedTile):
    def __init__(self, pos, size, frames):
        super().__init__(pos, size, frames)
        self.frame_speed = 0.1
        self.speed = 1

    def reverse(self):
        # accessed outside class
        self.speed *= -1

    def update(self, x_shift):
        self.rect.x += x_shift
        self.animate()
        # move
        self.rect.x += self.speed
        if self.speed > 0:
            self.image = pg.transform.flip(self.image, True, False)
