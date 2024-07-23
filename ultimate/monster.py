import pygame
from itertools import cycle
from typing import Dict, Tuple
from lib.asset import Static
from enum import StrEnum
from lib.types import Coordinate
from player import Player
from lib.scorebar import ScoreBar


class Monster(Static):
    def __init__(
        self,
        player: Player,
        score: ScoreBar,
        images: Dict[str, pygame.Surface],
        state: str,
        speed: Tuple[int, int] = (0, 0),
        damage: float = 1.0,
        run_animation_speed: int = 20,
    ) -> None:
        super().__init__(images, state)
        self.player = player
        self.score = score
        self.speed_x, self.speed_y = speed
        self.damage = damage
        self.current_frame = 0
        self.run_animation_speed = run_animation_speed

    def start_at(self, c: Coordinate) -> None:
        self.rect.bottomleft = c

    def _check_borders(self) -> None:
        screen_width, screen_height = pygame.display.get_window_size()
        pos_x, pos_y = self.rect.center
        if (
            pos_x <= -100
            or pos_y <= -100
            or pos_x >= screen_width + 100
            or pos_y >= screen_height + 100
        ):
            self.score.add(1)
            self.kill()

    def _run_animation(self) -> None:
        self.current_frame += 1
        if self.current_frame >= self.run_animation_speed:
            self.current_frame = 0
            self.set_state(self.run_cycle.__next__())

    def move(self) -> None:
        self._check_borders()
        pos_x, pos_y = self.rect.center
        self.rect.center = (pos_x + self.speed_x, pos_y + self.speed_y)

    def update(self) -> None:
        if self.rect.colliderect(self.player.rect):
            if pygame.sprite.collide_mask(self.player, self):
                self.player.take_damage(self.damage)
        self.move()


class Snail(Monster):
    class State(StrEnum):
        HATCHED = "hatched"
        RUN1 = "run1"
        RUN2 = "run2"
        DEAD = "dead"

    run_cycle = cycle([State.RUN1, State.RUN2])

    def move(self) -> None:
        self._check_borders()
        self._run_animation()
        pos_x, pos_y = self.rect.center
        self.rect.center = (pos_x + self.speed_x, pos_y + self.speed_y)


class Fly(Monster):
    class State(StrEnum):
        RUN1 = "run1"
        RUN2 = "run2"
        DEAD = "dead"

    _range = list(range(-5, 6))
    _current = 5
    _direction = 1

    run_cycle = cycle([State.RUN1, State.RUN2])

    def move(self) -> None:
        self._check_borders()
        self._run_animation()
        pos_x, pos_y = self.rect.center
        offset_y = self._range[self._current]
        if self._current == 0 or self._current == len(self._range) - 1:
            self._direction *= -1
        self._current += 1 * self._direction

        self.rect.center = (pos_x + self.speed_x, pos_y + self.speed_y + offset_y)
