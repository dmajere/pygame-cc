from __future__ import annotations
import sys
import pygame
from typing import Tuple, Union
import math

pygame.init()
clock = pygame.time.Clock()

screen_width = 400
screen_height = 300
FRAME_RATE = 60
screen = pygame.display.set_mode((screen_width, screen_height))

Coordinate = Tuple[int, int]
Vector = pygame.math.Vector2
OptionalInt = Union[None, int]


class Particle(pygame.sprite.Sprite):
    def __init__(
        self,
        x: int,
        y: int,
        radius: int,
        collision_tolerance: float = 0,
        container: pygame.Rect = None,
    ) -> None:
        super().__init__()

        self.pos: Coordinate = (x, y)
        self.radius = radius
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, (59, 220, 203), (radius, radius), radius)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.dt = 1

        self.collision_tolerance = collision_tolerance
        self.container = container

        self.vel = Vector(-2, 1)
        self.acc = Vector(0, 0)

    def calc_vel(self, v: Vector, a: Vector, dt: int = 1) -> Vector:
        return Vector(
            v[0] + a[0] * dt,
            v[1] + a[1] * dt,
        )

    def calc_pos(self, p: Coordinate, v: Vector, dt: int = 1) -> Coordinate:
        return Vector(
            int(p[0] + v[0] * dt),
            int(p[1] + v[1] * dt),
        )

    def calc_distance(self, a: Coordinate, b: Coordinate) -> int:
        x0, y0 = a
        x1, y1 = b
        return math.sqrt(pow(abs(x0 - x1), 2) + pow(abs(y0 - y1), 2))

    def calc_box_collision_point(
        self, a: Coordinate, b: Coordinate, plane: Tuple[OptionalInt, OptionalInt]
    ) -> Coordinate:
        x0, y0 = a
        x1, y1 = b
        xp, yp = plane

        k0, k1, p = (x0, x1, xp) if yp is None else (y0, y1, yp)

        tc = (p + self.radius - k1) / abs(k0 - k1) / FRAME_RATE
        return self.calc_pos(a, self.vel, tc)

    def calc_box_reflection(
        self, a: Coordinate, b: Coordinate, plane: Tuple[OptionalInt, OptionalInt]
    ) -> Coordinate:
        dx = a[0] - b[0]
        dy = a[1] - b[1]

        if plane[0] is None:
            return (b[0], a[1] + dy)
        elif plane[1] is None:
            return (a[0] + dx, b[1])

    def calc_box_collision_pos(
        self, a: Coordinate, b: Coordinate, plane: Tuple[OptionalInt, OptionalInt]
    ) -> Coordinate:
        col_point = self.calc_box_collision_point(a, b, plane)
        ref_point = self.calc_box_reflection(col_point, b, plane)
        return ref_point

    def handle_box_collision(self, pos: Coordinate) -> Coordinate:
        if self.container:
            if pos[1] - self.container.top < self.radius:
                pos = self.calc_box_collision_pos(
                    self.rect.center, pos, (None, self.container.top)
                )
                self.vel.update(self.vel[0], -self.vel[1])

            if abs(pos[1] - self.container.bottom) < self.radius:
                pos = self.calc_box_collision_pos(
                    self.rect.center, pos, (None, self.container.bottom)
                )
                self.vel.update(self.vel[0], -self.vel[1])

            if pos[0] - self.container.left < self.radius:
                pos = self.calc_box_collision_pos(
                    self.rect.center, pos, (self.container.left, None)
                )
                self.vel.update(-self.vel[0], self.vel[1])

            if abs(pos[0] - self.container.right) < self.radius:
                pos = self.calc_box_collision_pos(
                    self.rect.center, pos, (self.container.right, None)
                )
                self.vel.update(-self.vel[0], self.vel[1])
        return pos

    def is_particle_collided(self, other: Particle) -> bool:
        return self.calc_distance(self.pos, other.pos) <= (self.radius + other.radius)

    def calc_postcol_vel(self, other: Particle) -> Vector:
        # def _calc_vel(v1, m1, v2, m2, c1, c2) -> int:
        # (2 * m2 / (m1 + m2)) *
        # self.vel
        pass

    def update(self) -> None:
        self.vel = self.calc_vel(self.vel, self.acc, self.dt)
        self.pos = self.handle_box_collision(self.calc_pos(self.pos, self.vel, self.dt))

        self.rect.center = self.pos


container_rect = pygame.Rect(0, 0, screen_width, screen_height)
partiles = pygame.sprite.Group()
p1 = Particle(
    100,
    100,
    10,
    container=container_rect,
)
partiles.add(p1)
# p2 = Particle(
# 200, 200, 20,
# container=container_rect,
# )
# partiles.add(p2)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill((255, 255, 255))
    partiles.draw(screen)
    partiles.update()

    pygame.display.flip()
    clock.tick(FRAME_RATE)
