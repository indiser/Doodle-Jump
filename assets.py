import pygame
import os
from config import *

def get_path(filepath: str):
    return os.path.join(os.path.dirname(__file__), filepath)


background = pygame.image.load(get_path('Game_Assests/sprites/background.png'))

doodle = pygame.image.load(get_path('Game_Assests/sprites/right.png'))
doodle = pygame.transform.scale(doodle, (DOODLE_WIDTH, DOODLE_HEIGHT))

platform = pygame.image.load(get_path('Game_Assests/sprites/platform.png'))
platform = pygame.transform.scale(platform, (PLATFORM_WIDTH, PLATFORM_HEIGHT))

feeder_down = pygame.image.load(get_path('Game_Assests/sprites/feder.png'))
feeder_up = pygame.image.load(get_path('Game_Assests/sprites/feder_up.png'))