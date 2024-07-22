import pygame
from typing import List
from .types import Coordinate


class ScoreBar:
    def __init__(
        self,
        width: int,
        height: int,
        digits: List[pygame.Surface],
        max_digits: int = 3,
    ) -> None:
        self.width = width
        self.height = height
        self.digits = [
            pygame.transform.scale(d, (self.width, self.height)) for d in digits
        ]

        self.max_digits = max_digits
        self.max_value = int(self.max_digits * "9")
        self.value = 0
        self.bar_rect = pygame.rect.Rect(
            0, 0, self.max_digits * self.width, self.height
        )

    def draw(self, surface: pygame.Surface, c: Coordinate) -> None:
        bar_width = self.max_digits * self.width
        bar_surface = pygame.Surface(
            (bar_width, self.height), pygame.SRCALPHA, 32
        ).convert_alpha()
        value_str = str(self.value)
        value_str = (self.max_digits - len(value_str)) * "0" + value_str
        for idx, d in enumerate(value_str):
            d = int(d)
            bar_surface.blit(self.digits[d], (idx * self.width - 10 * idx, 0))

        self.bar_rect.center = c
        pygame.draw.rect(surface, (255, 255, 255), self.bar_rect, -1)
        surface.blit(bar_surface, self.bar_rect)

    def add(self, v: int) -> None:
        self.value = min(self.max_value, self.value + v)
