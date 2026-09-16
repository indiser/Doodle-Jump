import pygame
from config import HEIGHT, WIDTH
from assets import *
import random
from Doodle import Player
from Platform import Platform, ExplodingPlatform, MovingPlatform
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

broken_frames = [broken_platform0, broken_platform1, broken_platform2, broken_platform3]

explosive_frames = [exploding_platform0, exploding_platform1, exploding_platform2]

def make_platform(x, y, current_score):
    roll = random.randint(1, 100)
    
    if roll <= 10:   # 10% Horizontal
        return MovingPlatform(x, y, horizental_platform, 'horizontal', current_score)
    elif roll <= 20: # 10% Vertical
        return MovingPlatform(x, y, vertical_platform, 'vertical', current_score)
    elif roll <= 35: # 15% Explosive
        return ExplodingPlatform(x, y, explosive_frames)
    elif roll <= 50: # 15% Broken
        return Platform(x, y, broken_platform0, breakable=True, broken_frames=broken_frames)
        
    return Platform(x, y, platform)

start_x = screen_rect.centerx - (PLATFORM_WIDTH // 2)
start_y = screen_rect.bottom - 20
start_p = Platform(start_x, start_y, platform)
platforms.append(start_p)

player = Player(screen_rect.centerx, start_p.rect.top, doodle_right, doodle_left)

current_y = start_p.rect.top
while current_y > 0:
    gap = random.randint(60, 120)
    current_y -= gap
    p_x = random.randint(0, WIDTH - PLATFORM_WIDTH)
    platforms.append(make_platform(p_x, current_y, score))



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
                if not p.broken and player.rect.colliderect(p.rect):
                    player.rect.bottom = p.rect.top
                    player.jump(JUMP_STRENGTH)
                    if p.breakable:
                        p.break_platform()
                    break

    # --- 2.5 UPDATE/CLEANUP PLATFORMS (every frame) ---
    for p in platforms[:]:
        p.update()
        if p.finished or p.rect.top >= HEIGHT:
            platforms.remove(p)

            new_x = random.randint(0, WIDTH - PLATFORM_WIDTH)
            highest_y = min([plat.rect.y for plat in platforms])
            new_y = highest_y - random.randint(60, 120)
            new_plat = make_platform(new_x, new_y, score)
            platforms.append(new_plat)

            if type(new_plat) is Platform and not new_plat.breakable and score > FEEDER_THRESHOLD and random.randint(1, 10) == 1:
                new_feeder = Feeder(new_plat.rect.centerx, new_plat.rect.top, feeder_down, feeder_up)
                active_feeders.append(new_feeder)

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
                new_plat = make_platform(new_x, new_y, score)
                platforms.append(new_plat)

                # Spawn Feeder on top of the new platform
                if type(new_plat) is Platform and not new_plat.breakable and score > FEEDER_THRESHOLD and random.randint(1, 10) == 1:
                    new_feeder = Feeder(new_plat.rect.centerx + 15, new_plat.rect.top - 5, feeder_down, feeder_up)
                    active_feeders.append(new_feeder)

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