import pygame
from config import HEIGHT, WIDTH
from assets import *
import random
from Doodle import Player
from Platform import Platform
from Feeder import Feeder

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
screen_rect = screen.get_rect()
platform_rect = platform.get_rect()
running = True

platforms = []
active_feeders = []
score = 0

start_x = screen_rect.centerx - (PLATFORM_WIDTH // 2)
start_y = screen_rect.bottom - 20
start_p = Platform(start_x, start_y, platform)
platforms.append(start_p)

player = Player(screen_rect.centerx, start_p.rect.top, doodle)

current_y = start_p.rect.top
while current_y > 0:
    gap = random.randint(60, 120) 
    current_y -= gap
    p_x = random.randint(0, WIDTH - PLATFORM_WIDTH)
    platforms.append(Platform(p_x, current_y, platform))


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- 1. INPUT & PHYSICS ---
    keys = pygame.key.get_pressed()
    player.move(keys, MOVE_SPEED, WIDTH)
    player.apply_gravity(GRAVITY)

    # --- 2. COLLISIONS ---
    if player.y_velocity > 0:
        hit_feeder = False
        for f in active_feeders:
            if player.rect.colliderect(f.rect):
                player.rect.bottom = f.rect.top
                player.jump(JUMP_STRENGTH, boost_multiplier=1.8)
                f.trigger()  # Feeder handles its own state
                hit_feeder = True
                break

        if not hit_feeder:
            for p in platforms:
                if player.rect.colliderect(p.rect):
                    player.rect.bottom = p.rect.top
                    player.jump(JUMP_STRENGTH)
                    break

    # --- 3. CAMERA & WORLD SHIFT ---
    scroll_threshold = HEIGHT // 3
    if player.rect.top <= scroll_threshold:
        player.rect.top = scroll_threshold
        
        # Invert the negative upward velocity to create positive downward shift
        shift = player.y_velocity 
        score -= shift

        # Shift platforms and handle generation
        for p in platforms[:]:
            p.scroll(shift)
            if p.rect.top >= HEIGHT:
                platforms.remove(p)
                
                new_x = random.randint(0, WIDTH - PLATFORM_WIDTH)
                highest_y = min([plat.rect.y for plat in platforms]) 
                new_y = highest_y - random.randint(60, 120)
                new_plat = Platform(new_x, new_y, platform)
                platforms.append(new_plat)

                # Spawn Feeder on top of the new platform
                if score > FEEDER_THRESHOLD and random.randint(1, 10) == 1:
                    # Feeder __init__ takes x and y for midbottom
                    new_feeder = Feeder(new_plat.rect.centerx, new_plat.rect.top, feeder_down, feeder_up)
                    active_feeders.append(new_feeder)

        # Shift feeders and clean up
        for f in active_feeders[:]:
            f.scroll(shift)
            if f.rect.top >= HEIGHT:
                active_feeders.remove(f)

    # --- 4. RENDER ---
    screen.blit(background, (0, 0))

    for p in platforms:
        p.draw(screen)
    for f in active_feeders:
        f.draw(screen)
        
    player.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()