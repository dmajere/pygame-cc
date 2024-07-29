from typing import Tuple
from settings import TILE_SIZE
import pygame


class Sprite(pygame.sprite.Sprite):
    def __init__(
        self,
        pos: Tuple[int, int],
        surface: pygame.Surface,
        *groups: pygame.sprite.Group,
        size: Tuple[int, int] = (TILE_SIZE, TILE_SIZE)
    ) -> None:
        super().__init__(*groups)

        self.image = surface.convert_alpha()
        self.rect = self.image.get_frect(topleft=pos)
