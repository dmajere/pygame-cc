import pygame
from common import Game
from typing import Tuple


class BouncingRect(pygame.Rect):

    def set_speed(self, x, y):
        self.speed_x = x
        self.speed_y = y

    def should_bounce_screen(self, screen: pygame.Surface) -> Tuple[bool, bool]:
        w = screen.get_width()
        h = screen.get_height()
        x, y = False, False
        if self.right >= w or self.left <= 0:
            x = True
        if self.bottom >= h or self.top <= 0:
            y = True
        return (x, y)

    def should_bounce_rect(self, other: pygame.Rect) -> Tuple[bool, bool]:
        collision_tolerance = 10
        x, y = False, False
        if self.colliderect(other):
            if abs(self.top - other.bottom) < collision_tolerance and self.speed_y < 0:
                y = True
            if abs(self.bottom - other.top) < collision_tolerance and self.speed_y > 0:
                y = True
            if abs(self.right - other.left) < collision_tolerance and self.speed_x > 0:
                x = True
            if abs(self.left - other.right) < collision_tolerance and self.speed_x < 0:
                x = True
        return x, y

    def move(self, screen: pygame.Surface, other: pygame.Rect = None) -> None:
        alter_x, alter_y = self.should_bounce_screen(screen)
        self.speed_x *= -1 if alter_x else 1
        self.speed_y *= -1 if alter_y else 1
        if other:
            alter_x, alter_y = self.should_bounce_rect(other)
            self.speed_x *= -1 if alter_x else 1
            self.speed_y *= -1 if alter_y else 1

        self.x += self.speed_x
        self.y += self.speed_y


class Collision(Game):
    def init(self) -> None:
        self.rect_a = BouncingRect(350, 350, 100, 100)
        self.rect_a.set_speed(5, 4)
        self.rect_b = BouncingRect(300, 600, 200, 100)
        self.rect_b.set_speed(0, 2)

    def bounce(
        self, rect: pygame.Rect, speed_x, speed_y, other: pygame.Rect = None
    ) -> Tuple[int, int]:

        rect.x += speed_x
        rect.y += speed_y
        return speed_x, speed_y

    def run(self) -> None:
        def _run(self) -> None:
            self.screen.fill((30, 30, 30))
            pygame.draw.rect(self.screen, (255, 255, 255), self.rect_a)
            pygame.draw.rect(self.screen, (255, 0, 0), self.rect_b)
            self.rect_a.move(self.screen, self.rect_b)
            self.rect_b.move(self.screen)

        events = {}
        self._loop(_run, events=events)


game = Collision(800, 800)
game.run()
