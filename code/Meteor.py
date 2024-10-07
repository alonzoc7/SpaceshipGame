import pygame 
from random import randint, uniform
from os.path import join

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720

class Meteor(pygame.sprite.Sprite):
    def __init__(self, groups, img):
        super().__init__(groups)
        self.original_surf = img
        self.image = self.original_surf
        self.rect = self.image.get_frect(center = (randint(40, WINDOW_WIDTH-40), 0))
        self.created_time = pygame.time.get_ticks()
        self.speed = randint(200,700)
        self.direction = pygame.Vector2(uniform(-0.5, 0.5),1)
        self.rotation_speed = randint(30, 70)
        self.rotation = 0

    def update(self, key_press, dt):
        self.rect.center += self.direction*self.speed*dt
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()
        # Rotate the meteors
        self.rotation += self.rotation_speed*dt
        self.image = pygame.transform.rotozoom(self.original_surf, self.rotation, 1)
        # We have to update the rect as well as the image to avoid weird shaking of the image
        self.rect = self.image.get_rect(center = self.rect.center)
        



