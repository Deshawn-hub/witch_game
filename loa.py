import random
import pygame
import os

pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

# File paths
sprite_sheet_path = os.path.join("C:/Users/desha/OneDrive/Desktop/pygamec", "Edwina128x128.png")
background_path = "background.png"
cloud_path = "cloud.png"

# Load assets
sprite_sheets = pygame.image.load(sprite_sheet_path).convert_alpha()
background = pygame.image.load(background_path).convert_alpha()
resize_background = pygame.transform.scale(background, (800, 800))
cloud = pygame.image.load(cloud_path).convert_alpha()
cloud_resize = pygame.transform.scale(cloud, (270, 270))
play_btn = pygame.image.load('Game UI Blue Button Set Open-01.png')

black = (0, 0, 0)
running = True
Load_screen = True
dt = 0

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x_velocity = -5
        self.sprites = []

        for i in range(1, 9):
            transfrom_enmy = pygame.image.load(f"frame-{i}.png").convert_alpha()
            resize_img = pygame.transform.scale(transfrom_enmy, (50, 50))
            fliped_img = pygame.transform.flip(resize_img, True, False)
            self.sprites.append(fliped_img)

        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        self.rect.x += self.x_velocity
        if self.rect.right < 0:
            self.kill()  # Remove the enemy if it goes off-screen
        self.current_sprite += 1
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

class Clouds(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.x_velocity = random.randint(-5, -2)  # Random speed for clouds

    def update(self):
        self.rect.x += self.x_velocity
        if self.rect.right < 0:
            self.rect.left = 800

class SpriteSheet(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.sheet = image
        self.sprites = []
        self.current_sprite = 0

        for i in range(5):
            self.sprites.append(self.get_image(i, 128, 128, 3, black))

        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect(topleft=(x, y))

    def get_image(self, frame, width, height, scale, col):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (104,104))
        image.set_colorkey(col)
        return image

    def update(self, enemy):
        global running
        global Load_screen
        self.current_sprite += 1/3
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]

        for i in enemy:
            if self.rect.colliderect(i.rect):

                running = False

    def move(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= 300 * dt
        if keys[pygame.K_DOWN] and self.rect.bottom < 800:
            self.rect.y += 300 * dt

class SpriteSheet1(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.sheet = image
        self.sprites = []
        self.current_sprite = 0

        for i in range(5):
            self.sprites.append(self.get_image(i, 128, 128, 3, black))

        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect(topleft=(x, y))

    def get_image(self, frame, width, height, scale, col):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image,(400, 400))
        image.set_colorkey(col)
        return image

    def update(self):
        self.current_sprite += 1/3
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]

      
   


# Create sprite groups
moving_sprites = pygame.sprite.Group()
startingsprite = pygame.sprite.Group()
clouds_sprite = pygame.sprite.Group()
enemy_sprite = pygame.sprite.Group()

# Add sprites to the groups
SpS = SpriteSheet(sprite_sheets, 0, 0)
SpS1 = SpriteSheet1(sprite_sheets, 0, 0)
moving_sprites.add(SpS)
startingsprite.add(SpS1)

cloud1 = Clouds(cloud_resize, 800, 100)
cloud2 = Clouds(cloud_resize, 1200, 300)
cloud3 = Clouds(cloud_resize, 1500, 500)
clouds_sprite.add(cloud1, cloud2, cloud3)

# Enemy spawn timer
enemy_spawn_time = 2000  # Spawn an enemy every 2 seconds
last_enemy_spawn = pygame.time.get_ticks()
ran_cordinate = (100, 700, 800, 200, 300, 400)

# Load screen loop
while Load_screen:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:  # Press any key to start the game
            Load_screen = False
        if event.type == pygame.QUIT:
            Load_screen = False
            running = False
    
    screen.blit(resize_background, (0, 0))
    screen.blit(play_btn,(600,100))
    startingsprite.draw(screen)
    startingsprite.update()
    
    pygame.display.flip()


        

# Main game loop
while running:
    dt = clock.tick(60) / 1000  # Delta time in seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    

    # Spawn enemies at intervals
    current_time = pygame.time.get_ticks()
    if current_time - last_enemy_spawn > enemy_spawn_time:
        enemy = Enemy(800, random.choice(ran_cordinate))
        enemy_sprite.add(enemy)
        last_enemy_spawn = current_time

    # Draw background
    screen.blit(resize_background, (0, 0))

    # Draw and update clouds
    clouds_sprite.draw(screen)
    clouds_sprite.update()

    # Draw and update enemies
    enemy_sprite.draw(screen)
    enemy_sprite.update()

    # Draw and update sprite sheet animation
    moving_sprites.draw(screen)
    moving_sprites.update(enemy_sprite)
    SpS.move(dt)

    pygame.display.flip()

pygame.quit()