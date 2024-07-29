from typing import Tuple
import pygame
from pygame.sprite import Group
from pygame.math import Vector2 as vector
from sprite import Sprite
from enum import IntEnum


class Axis:
    Horizontal = 0
    Vertical = 1


class Player(Sprite):
    def __init__(
        self,
        pos: Tuple[int, int],
        surface: pygame.Surface,
        collision_sprites: pygame.sprite.Group,
        *groups: Group
    ) -> None:
        super().__init__(
            pos, surface, *groups, size=(surface.get_width(), surface.get_height())
        )
        self.direction = vector(0, 0)
        self.speed = 200
        self.gravity = 1300

        self.collision_sprites = collision_sprites

    def input(self) -> None:
        keys = pygame.key.get_pressed()

        input_vector = vector(0, 0)
        if keys[pygame.K_LEFT]:
            input_vector.x -= 1
        if keys[pygame.K_RIGHT]:
            input_vector.x += 1
        self.direction.x = (
            input_vector.normalize().x if input_vector else input_vector.x
        )

    def move(self, dt: float) -> None:
        self.rect.x += self.direction.x * self.speed * dt
        self.collision(Axis.Horizontal)

        self.direction.y += self.gravity / 2 * dt
        self.rect.y += self.direction.y * dt
        self.direction.y += self.gravity / 2 * dt
        self.collision(Axis.Vertical)

    def collision(self, axis: Axis):
        for sprite in self.collision_sprites:
            if self.rect.colliderect(sprite.rect):
                if axis == Axis.Horizontal:
                    if self.rect.left <= sprite.rect.right and self.direction.x < 0:
                        self.rect.left = sprite.rect.right
                    elif self.rect.right >= sprite.rect.left and self.direction.x > 0:
                        self.rect.right = sprite.rect.left
                else:  # Axis.Vertical
                    if self.rect.top <= sprite.rect.bottom and self.direction.y < 0:
                        self.rect.top = sprite.rect.bottom
                    elif self.rect.bottom >= sprite.rect.top and self.direction.y >= 0:
                        self.rect.bottom = sprite.rect.top
                        self.direction.y = 0
                    # self.direction.y  = 0 # Check if we need to move it out of else

    def update(self, dt: float) -> None:
        self.input()
        self.move(dt)
