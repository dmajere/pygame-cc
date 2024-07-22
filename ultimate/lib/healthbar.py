import pygame
from .types import Color, Coordinate


class HealthBar:
    def __init__(
        self,
        width: int,
        height: int,
        color: Color,
        background_color: Color = (255, 255, 255),
        border_width: int = 2,
        start_health: int = 100,
        limit_health: int = 100,
        icon: pygame.Surface = None,
    ) -> None:
        self.width = width
        self.height = height
        self.color = color
        self.border_width = border_width
        self.current_health = start_health
        self.limit_health = limit_health
        self.background_color = background_color
        self.icon = pygame.transform.scale(
            icon, (height * 2, height * 2)
        ).convert_alpha()

        self.health_rect = pygame.rect.Rect(0, 0, self.width, self.height)

    def draw(self, surface: pygame.Surface, c: Coordinate) -> None:
        health_left = self.current_health / self.limit_health
        health_width = int(self.width * health_left)

        health_surface = pygame.Surface((health_width, self.height))
        health_surface.fill(self.color)
        self.health_rect.center = c

        pygame.draw.rect(surface, self.background_color, self.health_rect)
        pygame.draw.rect(surface, self.color, self.health_rect, self.border_width)
        surface.blit(health_surface, self.health_rect)

        x, y = self.health_rect.bottomright
        if self.icon:
            surface.blit(
                self.icon, (x - self.icon.get_width() // 2, y - self.icon.get_height())
            )

    def add_damage(self, amount: int) -> None:
        self.current_health -= amount
        self.current_health = max(self.current_health, 0)

    def set_health(self, health: int) -> None:
        health = min(health, self.limit_health)
        self.current_health = health
