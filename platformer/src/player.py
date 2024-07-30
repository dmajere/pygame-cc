from typing import Tuple, Dict
import pygame
from pygame.sprite import Group
from pygame.math import Vector2 as vector
from sprite import Sprite
from enum import IntEnum
from util import Timer


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

        self.jump = False
        self.jump_height = 800
        self.on_surface = {"floor": False, "left": False, "right": False}

        self.collision_sprites = collision_sprites
        self.collision_rects = [sprite.rect for sprite in self.collision_sprites]

        self.timer: Dict[str, Timer] = {
            "in_wall_jump": Timer(400),
            "in_jump": Timer(120),
        }

    def input(self) -> None:
        keys = pygame.key.get_pressed()

        input_vector = vector(0, 0)
        if not self.timer["in_wall_jump"].active:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                input_vector.x -= 1
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                input_vector.x += 1
            self.direction.x = (
                input_vector.normalize().x if input_vector else input_vector.x
            )

        if keys[pygame.K_SPACE]:
            self.jump = True

    def move(self, dt: float) -> None:
        self.rect.x += self.direction.x * self.speed * dt
        self.collision(Axis.Horizontal)

        if (
            not self.on_surface["floor"]
            and any((self.on_surface["left"], self.on_surface["right"]))
            and not self.timer["in_jump"].active
        ):
            # wall slide
            self.direction.y = 0
            self.rect.y += self.gravity / 10 * dt
        else:
            # basic gravity
            self.direction.y += self.gravity / 2 * dt
            self.rect.y += self.direction.y * dt
            self.direction.y += self.gravity / 2 * dt
        self.collision(Axis.Vertical)

        if self.jump:
            if self.on_surface["floor"]:
                # floor jump
                self.timer["in_jump"].activate()
                self.direction.y = -self.jump_height
            # elif any((self.on_surface['left'], self.on_surface['right'])) and not self.timer['wall_slide'].active:
            elif (
                any((self.on_surface["left"], self.on_surface["right"]))
                and not self.timer["in_jump"].active
            ):
                self.timer["in_wall_jump"].activate()
                self.direction.y = -self.jump_height
                self.direction.x = 1 if self.on_surface["left"] else -1
            self.jump = False

    def check_surface_contact(self) -> None:
        bottom_r = pygame.rect.Rect((self.rect.bottomleft), (self.rect.width, 2))
        left_r = pygame.rect.Rect(
            (self.rect.topleft + vector(-2, self.rect.height / 4)),
            (2, self.rect.height / 2),
        )
        right_r = pygame.rect.Rect(
            (self.rect.topright + vector(0, self.rect.height / 4)),
            (2, self.rect.height / 2),
        )

        srf = pygame.display.get_surface()
        pygame.draw.rect(srf, "yellow", bottom_r)
        pygame.draw.rect(srf, "yellow", left_r)
        pygame.draw.rect(srf, "yellow", right_r)

        self.on_surface["floor"] = bottom_r.collidelist(self.collision_rects) >= 0
        self.on_surface["right"] = right_r.collidelist(self.collision_rects) >= 0
        self.on_surface["left"] = left_r.collidelist(self.collision_rects) >= 0

    def collision(self, axis: Axis):
        idx = self.rect.collidelist(self.collision_rects)
        if idx >= 0:
            rect = self.collision_rects[idx]
            if axis == Axis.Horizontal:
                if self.rect.left <= rect.right and self.direction.x < 0:
                    self.rect.left = rect.right
                elif self.rect.right >= rect.left and self.direction.x > 0:
                    self.rect.right = rect.left
            else:  # Axis.Vertical
                if self.rect.top <= rect.bottom and self.direction.y < 0:
                    self.rect.top = rect.bottom
                elif self.rect.bottom >= rect.top and self.direction.y >= 0:
                    self.rect.bottom = rect.top
                    self.direction.y = 0
                self.direction.y = 0  # Check if we need to move it out of else

    def update_timers(self) -> None:
        [timer.update() for timer in self.timer.values()]

    def update(self, dt: float) -> None:
        self.update_timers()
        self.check_surface_contact()

        self.input()
        self.move(dt)
