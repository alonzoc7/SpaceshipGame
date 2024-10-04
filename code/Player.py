import pygame 
from os.path import join
from Laser import Laser

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, laser_group, laser_surf, laser_sound):
        super().__init__(groups)
        player_img_path = join('images', 'player.png')
        self.image = pygame.image.load(player_img_path).convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
        # Usually want the player direction to be a very low value, and multiply it by the player speed
        self.direction = pygame.math.Vector2()
        self.speed = 300
        self.health = 100

        # Laser info for creating Laser object
        self.groups = groups
        self.laser_group = (groups, laser_group)
        self.laser_surf = laser_surf
        self.laser_sound = laser_sound
        self.on_cooldown = False
        self.laser_shoot_time = 0
        self.cooldown_duration = 400

    def laser_timer(self):
        if self.on_cooldown:
            if pygame.time.get_ticks() >= self.laser_shoot_time+self.cooldown_duration:
                self.on_cooldown = False
    
    def update(self, key_press, dt):
        # Capture Spaceship Movement
        if(key_press[pygame.K_w] or key_press[pygame.K_UP]):
            self.direction.y = -1
        elif(key_press[pygame.K_s] or key_press[pygame.K_DOWN]):
            self.direction.y = 1
        else:
            self.direction.y = 0

        if(key_press[pygame.K_a] or key_press[pygame.K_LEFT]):
            self.direction.x = -1
        elif(key_press[pygame.K_d] or key_press[pygame.K_RIGHT]):
            self.direction.x = 1
        else:
            self.direction.x = 0
        # Set direction to 1 if direction is any value besides (0,0), else keep it as is.
        self.direction = self.direction.normalize() if self.direction else self.direction
        # Change center value for movement
        self.rect.center += self.direction*self.speed*dt

        # Capture if the spacebar is pressed to shoot
        if pygame.key.get_just_pressed()[pygame.K_SPACE] and not self.on_cooldown:
            Laser(self.laser_group, self.laser_surf, self.rect.midtop)
            self.laser_shoot_time = pygame.time.get_ticks()
            self.on_cooldown = True 
            self.laser_sound.play()
        self.laser_timer()  

    def set_health(self, val):
        self.health += val

    def get_health(self):
        return self.health