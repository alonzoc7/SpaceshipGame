import pygame 
from random import randint, uniform
from os.path import join

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720

class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, groups, frames, pos):
        super().__init__(groups)
        # The animation always starts with the first frame
        self.frames = frames
        self.index = 0
        self.image = self.frames[self.index]
        self.position = pos
        self.rect = self.image.get_frect(center = self.position)

    def update(self, key_press, dt):
        self.index += 1
        if self.index < len(self.frames):
            self.image = self.frames[self.index]
        else:
            self.kill()
            