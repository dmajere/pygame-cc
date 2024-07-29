from typing import Tuple
import pygame
from pygame.sprite import Group
from pygame.math import Vector2 as vector
from sprite import Sprite


class Player(Sprite):
    def __init__(
        self, pos: Tuple[int, int], surface: pygame.Surface, *groups: Group
    ) -> None:
        super().__init__(
            pos, surface, *groups, size=(surface.get_width(), surface.get_height())
        )
        self.direction = vector(0, 0)
        self.speed = 200

    def input(self) -> None:
        keys = pygame.key.get_pressed()

        input_vector = vector(0, 0)
        if keys[pygame.K_LEFT]:
            input_vector.x -= 1
        if keys[pygame.K_RIGHT]:
            input_vector.x += 1
        self.direction = input_vector.normalize() if input_vector else input_vector

    def move(self, dt: float) -> None:
        print("DT", dt)
        self.rect.topleft += self.direction * self.speed * dt

    def update(self, dt: float) -> None:
        self.input()
        self.move(dt)
