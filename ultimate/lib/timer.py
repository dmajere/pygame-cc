import pygame
from typing import Callable


class Timer:
    def __init__(self, func: Callable, second: int) -> None:
        self._threshold = second * 1000
        self._last_trigger = 0
        self._func = func
        self._pause = True

    @property
    def current_time(self) -> int:
        return pygame.time.get_ticks()

    def tick(self):
        if not self._pause and (
            self.current_time - self._last_trigger >= self._threshold
        ):
            self._func()
            self._last_trigger = self.current_time

    def stop(self) -> None:
        self._pause = True

    def start(self) -> None:
        self._pause = False
