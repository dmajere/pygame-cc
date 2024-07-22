import pygame
from typing import Dict, Tuple
from lib.asset import Static
from enum import StrEnum
from lib.types import Coordinate
from player import Player


class Monster(Static):

    def __init__(
        self,
        player: Player,
        images: Dict[str, pygame.Surface],
        state: str,
        speed: Tuple[int, int] = (0, 0),
        damage: float = 1.0,
    ) -> None:
        super().__init__(images, state)
        self.player = player
        self.speed_x, self.speed_y = speed
        self.damage = damage

    def start_at(self, c: Coordinate) -> None:
        self.rect.bottomleft = c

    def move(self) -> None:
        screen_width, screen_height = pygame.display.get_window_size()
        pos_x, pos_y = self.rect.center
        if (
            pos_x <= -100
            or pos_y <= -100
            or pos_x >= screen_width + 100
            or pos_y >= screen_height + 100
        ):
            self.kill()
        self.rect.center = (pos_x + self.speed_x, pos_y + self.speed_y)

    def update(self) -> None:
        if self.rect.colliderect(self.player.rect):
            if pygame.sprite.collide_mask(self.player, self):
                self.player.take_damage(self.damage)
        self.move()


class Snail(Monster):
    class State(StrEnum):
        HATCHED = "hatched"
        RUN = "run"
        DEAD = "dead"
