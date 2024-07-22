from __future__ import annotations
import pygame
import pymunk
from typing import Tuple, List


class Timer:

    def __init__(self, clock: pygame.time.Clock, threshold: int = 2000) -> None:
        self.__clock = clock
        self.__threshold = threshold
        self.__event_time = 0

    def __repr__(self) -> str:
        return f"Timer(threshold={self.__threshold})"

    def __get_current_time(self) -> int:
        return pygame.time.get_ticks()

    @property
    def current_time(self) -> None:
        return self.__get_current_time()

    @property
    def is_expired(self) -> bool:
        return self.current_time - self.__event_time >= self.__threshold

    def trigger(self) -> None:
        self.__event_time = self.__get_current_time()


class Masked(Asset):
    def __init__(
        self,
        x: int,
        y: int,
        image: pygame.Surface,
        scale: Tuple[int, int] = None,
        shadow_color: Color = "grey",
    ) -> None:
        super().__init__(x, y, image=image, scale=scale)
        self.mask = pygame.mask.from_surface(self.image)
        self.shadowed = self.make_shadowed(self.mask, shadow_color)

    def make_shadowed(self, mask: pygame.mask.Mask, shadow_color: Color):
        shadowed = mask.to_surface()
        shadowed.set_colorkey((0, 0, 0))
        width, height = shadowed.get_size()
        for x in range(width):
            for y in range(height):
                color = shadowed.get_at((x, y))
                if color != (0, 0, 0, 255):
                    shadowed.set_at((x, y), shadow_color)
        return shadowed


class Physical(Asset):
    def __init__(
        self,
        x: int,
        y: int,
        radius: int,
        image: pygame.Surface,
        space: pymunk.Space,
        mass: float = 0,
        inertia: float = 0,
        body_type: int = pymunk.Body.DYNAMIC,
        scale: Tuple[int, int] = None,
    ) -> None:
        super().__init__(x, y, image=image, scale=scale)

        self.body = pymunk.body.Body(mass, inertia, body_type=body_type)
        self.body.position = (x, y)
        self.shape = pymunk.Circle(self.body, radius)
        self.space = space
        self.space.add(self.body, self.shape)

    def update(self) -> None:
        self.rect.center = self.body.position

    def kill(self) -> None:
        self.space.remove(self.body, self.shape)
        super().kill()


class Rotating(Asset):
    def __init__(
        self, x: int, y: int, image: pygame.Surface, scale: Tuple[int, int] = None
    ) -> None:
        super().__init__(x, y, image=image, scale=scale)
        self.original_image = image
        self.angle = 0
        self.direction = 1

    def clockwise(self) -> None:
        self.direction = -1

    def counterclockwise(self) -> None:
        self.direction = 1

    def update(self):
        rotated = pygame.transform.rotozoom(
            self.original_image, angle=self.angle, scale=1
        )
        self.image = rotated
        self.rect = self.image.get_rect()
        self.rect.center = (self._pos_x, self._pos_y)
        self.angle += self.direction * 1


class TextBox:

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        x_margin: int = 3,
        active_color: pygame.Color = None,
        passive_color: pygame.Color = None,
        bg_color: pygame.Color = None,
        border: int = 0,
        default_text: str = "",
    ) -> None:
        self._pos_x, self._pos_y = x, y
        self.width, self.height = width, height
        self.rect = pygame.Rect(self._pos_x, self._pos_y, self.width, self.height)
        self.text = default_text
        self.active_color = active_color or pygame.Color(0, 0, 0)
        self.passive_color = passive_color or pygame.Color("gray15")
        self.bg_color = bg_color or pygame.Color(255, 255, 255)
        self.border = border
        self.font = pygame.font.Font(None, self.height)
        self.x_margin = x_margin
        self.min_box_size = 100

        self.active = False
        self.color = self.passive_color

    def toggle(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and not self.active:
                self.active = True
                self.text = ""
                self.color = self.active_color
            elif self.active:
                self.active = False
                self.color = self.passive_color

    def input(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_TAB:
                self.text += " "
            elif event.key == pygame.K_RETURN:
                self.process_text()
            else:
                self.text += event.unicode

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, self.bg_color, self.rect, self.border)
        textbox = self.font.render(self.text, True, self.color)
        x, y = self.rect.topleft
        screen.blit(textbox, (x + self.x_margin, y + self.height / 4 - 1))
        self.rect.width = max(
            self.min_box_size, textbox.get_width() + self.x_margin * 2
        )

    def process_text(self) -> None:
        self.text = ""
