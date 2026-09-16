import pygame
from config import HEIGHT, WIDTH
from assets import *
import random

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
screen_rect = screen.get_rect()
platform_rect = platform.get_rect()
running = True

platforms = []
start_platform = platform.get_rect()
start_platform.centerx = screen_rect.centerx
start_platform.bottom = screen_rect.bottom - 20
platforms.append(start_platform)

doodle_rect = doodle.get_rect()
doodle_rect.midbottom = start_platform.midtop

current_y = start_platform.top
while current_y > 0:
    gap = random.randint(60, 120) 
    current_y -= gap
    
    new_platform = platform.get_rect()
    new_platform.x = random.randint(0, WIDTH - PLATFORM_WIDTH)
    new_platform.y = current_y
    
    platforms.append(new_platform)

active_feeders = []
score = 0

class Player:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.y_velocity = 0

    def move(self, keys, move_speed, screen_width):
        if keys[pygame.K_LEFT]:
            self.rect.x -= move_speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += move_speed

        # Screen Wrap
        if self.rect.right < 0:
            self.rect.left = screen_width
        elif self.rect.left > screen_width:
            self.rect.right = 0

    def apply_gravity(self, gravity):
        self.y_velocity += gravity
        self.rect.y += self.y_velocity

    def jump(self, strength, boost_multiplier=1.0):
        self.y_velocity = strength * boost_multiplier

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Platform:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

    def scroll(self, amount):
        self.rect.y -= amount

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Feeder:
    def __init__(self, x, y, image_down, image_up):
        self.image_down = image_down
        self.image_up = image_up
        self.rect = self.image_down.get_rect(midbottom=(x, y))
        self.sprung = False

    def trigger(self):
        self.sprung = True

    def scroll(self, amount):
        self.rect.y -= amount

    def draw(self, surface):
        if self.sprung:
            surface.blit(self.image_up, self.rect)
        else:
            surface.blit(self.image_down, self.rect)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        doodle_rect.x -= MOVE_SPEED
    if keys[pygame.K_RIGHT]:
        doodle_rect.x += MOVE_SPEED

    if doodle_rect.right < 0:
        doodle_rect.left = WIDTH
    elif doodle_rect.left > WIDTH:
        doodle_rect.right = 0

    Y_VELOCITY += GRAVITY
    doodle_rect.y += Y_VELOCITY

    if Y_VELOCITY > 0:
        hit_feeder = False
        for f in active_feeders:
            if doodle_rect.colliderect(f["rect"]):
                doodle_rect.bottom = f["rect"].top
                Y_VELOCITY = JUMP_STRENGTH * 1.8  # Apply a massive 80% boost
                f["sprung"] = True                # Trigger the animation
                hit_feeder = True
                break

        if not hit_feeder:
            for p_rect in platforms:
                if doodle_rect.colliderect(p_rect):
                    doodle_rect.bottom = p_rect.top
                    Y_VELOCITY = JUMP_STRENGTH
                    break

    scroll_threshold = HEIGHT // 3
    if doodle_rect.top <= scroll_threshold:
        doodle_rect.top = scroll_threshold
        score -= Y_VELOCITY

        for p_rect in platforms:
            p_rect.y -= Y_VELOCITY
            if p_rect.top >= HEIGHT:
                platforms.remove(p_rect)
                new_platform = platform.get_rect()
                new_platform.x = random.randint(0, WIDTH - PLATFORM_WIDTH)
                highest_y = min([p.y for p in platforms]) 
                new_platform.y = highest_y - random.randint(60, 120)
                platforms.append(new_platform)

                if score > FEEDER_THRESHOLD and random.randint(1, 10) == 1:
                    f_rect = feeder_down.get_rect() 
                    f_rect.midbottom = new_platform.midtop
                    active_feeders.append({"rect": f_rect, "sprung": False})

        for f in active_feeders[:]:
            f["rect"].y -= Y_VELOCITY
            if f["rect"].top >= HEIGHT:
                active_feeders.remove(f)

    screen.blit(background, (0, 0))

    for p_rect in platforms:
        screen.blit(platform, p_rect)

    for f in active_feeders:
        if f["sprung"]:
            screen.blit(feeder_up, f["rect"])
        else:
            screen.blit(feeder_down, f["rect"])

    screen.blit(doodle, doodle_rect)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()