import pygame 
from random import randint
from os.path import join

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720

class Stars(pygame.sprite.Sprite):
    def __init__(self, groups, img):
        super().__init__(groups)
        self.image = img
        self.rect = self.image.get_frect(center = (randint(40, WINDOW_WIDTH-40), randint(40, WINDOW_HEIGHT-40)))
