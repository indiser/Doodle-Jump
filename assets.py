import pygame
import os
from config import *

def get_path(filepath: str):
    return os.path.join(os.path.dirname(__file__), filepath)


background = pygame.image.load(get_path('Game_Assests/sprites/background.png'))

doodle_right = pygame.image.load(get_path('Game_Assests/sprites/right.png'))
doodle_right = pygame.transform.scale(doodle_right, (DOODLE_WIDTH, DOODLE_HEIGHT))
doodle_left = pygame.image.load(get_path('Game_Assests/sprites/left.png'))
doodle_left = pygame.transform.scale(doodle_left, (DOODLE_WIDTH, DOODLE_HEIGHT))

# Platforms
platform = pygame.image.load(get_path('Game_Assests/sprites/platform.png'))
platform = pygame.transform.scale(platform, (PLATFORM_WIDTH, PLATFORM_HEIGHT))

broken_platform0 = pygame.image.load(get_path('Game_Assests/sprites/broken_platform0.png'))
broken_platform0 = pygame.transform.scale(broken_platform0, (PLATFORM_WIDTH, PLATFORM_HEIGHT))

broken_platform1 = pygame.image.load(get_path('Game_Assests/sprites/broken_platform1.png'))
broken_platform1 = pygame.transform.scale(broken_platform1, (PLATFORM_WIDTH, PLATFORM_HEIGHT))

broken_platform2 = pygame.image.load(get_path('Game_Assests/sprites/broken_platform2.png'))
broken_platform2 = pygame.transform.scale(broken_platform2, (PLATFORM_WIDTH, PLATFORM_HEIGHT))

broken_platform3 = pygame.image.load(get_path('Game_Assests/sprites/broken_platform3.png'))
broken_platform3 = pygame.transform.scale(broken_platform3, (PLATFORM_WIDTH, PLATFORM_HEIGHT))

exploding_platform0 = pygame.image.load(get_path('Game_Assests/sprites/explosive_platform0.png'))
exploding_platform0 = pygame.transform.scale(exploding_platform0, (PLATFORM_WIDTH, PLATFORM_HEIGHT))

exploding_platform1 = pygame.image.load(get_path('Game_Assests/sprites/explosive_platform1.png'))
exploding_platform1 = pygame.transform.scale(exploding_platform1, (PLATFORM_WIDTH, PLATFORM_HEIGHT))

exploding_platform2 = pygame.image.load(get_path('Game_Assests/sprites/explosive_platform2.png'))
exploding_platform2 = pygame.transform.scale(exploding_platform2, (PLATFORM_WIDTH, PLATFORM_HEIGHT))



feeder_down = pygame.image.load(get_path('Game_Assests/sprites/feder.png'))
feeder_down = pygame.transform.scale(feeder_down, (FEEDER_WIDTH, FEEDER_HEIGHT))
feeder_up = pygame.image.load(get_path('Game_Assests/sprites/feder_up.png'))
feeder_up = pygame.transform.scale(feeder_up, (FEEDER_WIDTH, FEEDER_HEIGHT))