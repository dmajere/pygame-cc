from enum import IntEnum
from pygame.math import Vector2 as vector

SCREEN_WIDHT: int = 1280
SCREEN_HEIGHT: int = 720
TILE_SIZE: int = 64
ANIMATION_SPEED: int = 6


class Layers(IntEnum):
    BG = 0
    CLOUDS = 1
    BG_TILES = 2
    PATH = 3
    BG_DETAIL = 4
    MAIN = 5
    WATER = 6
    FG = 7
