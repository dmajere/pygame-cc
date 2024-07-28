from __future__ import annotations
from typing import Union
from common import Game, Asset, Coordinate
from enum import IntEnum
import pygame


class Car(Asset):
    class Direction(IntEnum):
        LEFT = -1
        STRAIGHT = 0
        RIGHT = 1

    def __init__(
        self, x: int, y: int, image: pygame.Surface, scale: Coordinate = None
    ) -> None:
        super(Car, self).__init__(x, y, image, scale=scale)
        self.original_image = self.image

        self.angle = 0
        self.rotation_speed = 1.8
        self.direction = Car.Direction.STRAIGHT
        self.forward = pygame.math.Vector2(0, -1)
        self.active = False

    def move(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.direction = Car.Direction(self.direction + 1)
            if event.key == pygame.K_LEFT:
                self.direction = Car.Direction(self.direction - 1)
            if event.key == pygame.K_SPACE:
                self.active = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                self.direction = Car.Direction(self.direction - 1)
            if event.key == pygame.K_LEFT:
                self.direction = Car.Direction(self.direction + 1)
            if event.key == pygame.K_SPACE:
                self.active = False

    def set_rotation(self) -> None:
        if self.direction == Car.Direction.RIGHT:
            self.angle -= self.rotation_speed
        elif self.direction == Car.Direction.LEFT:
            self.angle += self.rotation_speed

        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def get_rotation(self) -> None:
        if self.direction == Car.Direction.RIGHT:
            self.forward.rotate_ip(self.rotation_speed)
        if self.direction == Car.Direction.LEFT:
            self.forward.rotate_ip(-self.rotation_speed)

    def accelerate(self) -> None:
        if self.active:
            self.rect.center += self.forward * 5

    def update(self) -> None:
        self.set_rotation()
        self.get_rotation()
        self.accelerate()


class GTA(Game):
    def init(self) -> None:
        self.car = pygame.sprite.GroupSingle(
            Car(100, 100, self.images.car, scale=(75, 75))
        )
        self.background = pygame.transform.scale(
            self.images.track, (self.screen.get_width(), self.screen.get_height())
        )

    def run(self) -> None:
        def _run(self) -> None:
            self.screen.fill("white")
            self.screen.blit(self.background, (0, 0))
            self.car.draw(self.screen)
            self.car.update()

        events = {
            pygame.KEYDOWN: self.car.sprite.move,
            pygame.KEYUP: self.car.sprite.move,
        }
        self._loop(_run, events=events)


images = {
    "car": "assets/car/Audi.png",
    "track": "assets/car/Track.png",
}
game = GTA(800, 600, images=images)
game.run()
