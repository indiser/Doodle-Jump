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

platform = pygame.image.load(get_path('Game_Assests/sprites/platform.png'))
platform = pygame.transform.scale(platform, (PLATFORM_WIDTH, PLATFORM_HEIGHT))

feeder_down = pygame.image.load(get_path('Game_Assests/sprites/feder.png'))
feeder_down = pygame.transform.scale(feeder_down, (FEEDER_WIDTH, FEEDER_HEIGHT))
feeder_up = pygame.image.load(get_path('Game_Assests/sprites/feder_up.png'))
feeder_up = pygame.transform.scale(feeder_up, (FEEDER_WIDTH, FEEDER_HEIGHT))