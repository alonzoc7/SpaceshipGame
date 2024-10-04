import pygame
from os.path import join
from Player import Player
from Stars import Stars
from Meteor import Meteor
from AnimatedExplosion import AnimatedExplosion

# Must start with init to initialize 
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption('Spaceship Game')
active = True
clock = pygame.time.Clock()

# Importing all images
# Import image with the correct path for the OS
star_img_path = join('images', 'star.png')
# Convert the image with convert (no transparent pixels) or convert_alpha (transparent pixels) to improve pygame performance
star_img = pygame.image.load(star_img_path).convert_alpha()
laser_img_path = join('images', 'laser.png')
laser_image = pygame.image.load(laser_img_path).convert_alpha()
meteor_img_path = join('images', 'meteor.png')
meteor_surface = pygame.image.load(meteor_img_path).convert_alpha()
font = pygame.font.Font(join('images', 'Oxanium-Bold.ttf'), 40)
explosion_surfaces = []
for i in range(21):
    expld_image_path = join('images', 'explosion', f'{i}.png')
    explosion_surfaces.append(pygame.image.load(expld_image_path).convert_alpha())

# Importing all sounds
laser_sound = pygame.mixer.Sound(join('audio', 'laser.wav'))
explosion_sound = pygame.mixer.Sound(join('audio', 'explosion.wav'))
damage_sound = pygame.mixer.Sound(join('audio', 'damage.ogg'))
music_sound = pygame.mixer.Sound(join('audio', 'game_music.wav'))

# Create background music channel
background_music = pygame.mixer.Channel(0)
background_music.play(music_sound)

# Creatinag a Group and adding all sprites
all_sprites = pygame.sprite.Group()
# Creating a separate meteor and laser sprite groups to distinguish collisions
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()

# Create 20 random stars
for i in range (20):
    Stars(all_sprites, star_img)
# Create Player Object
player = Player(all_sprites, laser_sprites, laser_image, laser_sound)

# Custom Meteor event to spawn meteors
meteor_spawn = pygame.event.custom_type()
# The first arg is what you want to trigger when the timer goes off, 2nd is the duration time in milliseconds (500=1/2 of 1 second)
pygame.time.set_timer(meteor_spawn, 500)
death_event = pygame.event.custom_type()

def laser_collision():
    for laser in laser_sprites:
        # 1st arg is a single sprite, 2nd is a group of sprites, 3rd is boolean to kill the sprite from the group that collided. Returns a list of collided sprites, letting you access them still for the rest of the frame
        collided_meteors = pygame.sprite.spritecollide(laser, meteor_sprites, True, pygame.sprite.collide_mask)
        for meteor in collided_meteors:
            pygame.sprite.spritecollide(meteor, laser_sprites, True, pygame.sprite.collide_mask)
            AnimatedExplosion(all_sprites, explosion_surfaces, laser.rect.midtop)
            explosion_sound.play()

def ship_collision():
    ship_damage = pygame.sprite.spritecollide(player, meteor_sprites, False, pygame.sprite.collide_mask)
    for items in ship_damage:
        player.set_health(-10)
        damage_sound.play()
    if player.get_health() <= 0:
        death_event()
    

def display_score(display_surface):
    current_time = int(pygame.time.get_ticks()/1000)
    text_surf = font.render(str(current_time), True, 'green')
    text_rect = text_surf.get_frect(midbottom= (WINDOW_WIDTH/2, WINDOW_HEIGHT-40))
    display_surface.blit(text_surf,text_rect)
    pygame.draw.rect(display_surface, 'black', text_rect.inflate(10, 10).move(0,-5), 3, 5)

while active:
    # Delta time
    dt = clock.tick(60)/1000
    # Event loop to check for inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
        if event.type == meteor_spawn:
            Meteor((meteor_sprites, all_sprites), meteor_surface)
        if event.type == death_event:
            AnimatedExplosion(all_sprites,explosion_surfaces,player.rect.center)
            explosion_sound.play()
            active = False

    key_press = pygame.key.get_pressed()
    all_sprites.update(key_press, dt)
    laser_collision()
    ship_collision()

    # Check if music needs to be looped
    if not background_music.get_busy():
        background_music.play(music_sound)
    
    # Draw the game
    display_surface.fill('lightpink3')
    display_score(display_surface)
    all_sprites.draw(display_surface)
    pygame.display.update()

# Always close the code with this even if the Quit event is captured to fully close anything being used by the program.
pygame.quit()