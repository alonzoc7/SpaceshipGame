import pygame 
from os.path import join

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720

class Laser(pygame.sprite.Sprite):
    def __init__(self, groups, img, pos):
        super().__init__(groups)
        # Import laser image
        self.image = img
        self.rect = self.image.get_frect(midbottom = pos)
        self.speed = 400

    def update(self, key_press, dt):
        self.rect.centery -= self.speed*dt
        if self.rect.bottom < 0:
            self.kill()