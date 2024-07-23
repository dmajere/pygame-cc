import pygame
from typing import Callable
from .types import Color, Coordinate


class Button:
    def __init__(
        self,
        color: Color,
        onClick: Callable = None,
        width: int = None,
        height: int = None,
        margin: int = None,
        border_width: int = None,
        border_radius: int = None,
        border_color: Color = (0, 0, 0),
        text: pygame.sprite.Sprite = None,
    ) -> None:
        self.width = width
        self.height = height

        self.border_width = (
            border_width if border_width is not None and border_width >= 0 else 0
        )
        self.border_radius = (
            border_radius if border_radius is not None and border_radius > 0 else -1
        )
        self.border_color = border_color

        self.margin = margin
        self.color = color
        self.text = text
        self.onClick = onClick
        self.rect = self._get_rect()

    def _get_rect(self) -> pygame.rect.Rect:
        if self.width and self.height:
            width, height = self.width, self.height
        elif self.margin and self.text:
            width, height = self.text.rect.width, self.text.rect.height
            width, height = width + self.margin, height + self.margin
        else:
            raise Exception(
                "Either width and height or margin and text must be specified"
            )
        if self.border_width:
            width, height = width + self.border_width, height + self.border_width
        return pygame.rect.Rect(0, 0, width, height)

    def draw(self, surface: pygame.Surface, c: Coordinate) -> None:
        self.rect.center = c
        self.text.rect.center = c

        pygame.draw.rect(
            surface, self.color, self.rect, border_radius=self.border_radius
        )
        if self.border_width > 0:
            pygame.draw.rect(
                surface,
                self.border_color,
                self.rect,
                width=self.border_width,
                border_radius=self.border_radius,
            )
        pygame.draw.rect(surface, self.color, self.text.rect, -1)
        surface.blit(self.text.image, self.text.rect)

    def process_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.onClick()
