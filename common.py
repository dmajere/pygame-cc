from __future__ import annotations
import sys
import pygame
import pymunk
from typing import Mapping, Callable, Tuple, List
from pathlib import Path

Color = Tuple[int, int, int]
Coordinate = Tuple[int, int]


class AttrDict(dict):
    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value


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


class Asset(pygame.sprite.Sprite):
    def __init__(
        self, x: int, y: int, image: pygame.Surface, scale: Tuple[int, int] = None
    ) -> None:
        super().__init__()
        self._pos_x = x
        self._pos_y = y

        self.image = image
        if scale:
            self.image = pygame.transform.scale(self.image, scale)
        self.rect = self.image.get_rect()
        self.rect.center = (self._pos_x, self._pos_y)


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


class Animation(pygame.sprite.Sprite):
    def __init__(
        self, x, y, frames: List[pygame.sprite.Sprite], frame_speed: float = 0.25
    ) -> None:
        super().__init__()

        self.frames = frames
        self.is_active = False
        self.frame_speed = frame_speed

        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self):
        if self.is_active:
            self._animate()

    def trigger(self):
        self.is_active = True

    def _animate(self):
        self.current_frame += self.frame_speed
        if self.current_frame >= len(self.frames):
            self.current_frame = 0
        self.image = self.frames[int(self.current_frame)]
        if self.current_frame == 0:
            self.is_active = False


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


class Game:
    def __init__(
        self,
        screen_width: int,
        screen_height: int,
        images: Mapping[str, Path] = None,
        sounds: Mapping[str, Path] = None,
        mouse_visible: bool = False,
        caption: str = "",
    ):
        self.clock = pygame.time.Clock()
        pygame.init()
        pygame.mouse.set_visible(mouse_visible)
        self.screen = pygame.display.set_mode((screen_width, screen_height))

        self.images: AttrDict = (
            self._load_assets(images, pygame.image.load) if images else AttrDict()
        )
        self.sounds: AttrDict = (
            self._load_assets(sounds, pygame.mixer.Sound) if sounds else AttrDict()
        )
        pygame.display.set_caption(caption)

        self.init()

    def _load_assets(self, assets: Mapping[str, Path], load_func: Callable):
        loaded = AttrDict()
        for key, path in assets.items():
            loaded[key] = load_func(path)
        return loaded

    def _process_exit(self, event: int) -> None:
        if event == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

    def _process_events(self, events: Mapping[int, Callable]) -> None:
        events = events or {}
        for event in pygame.event.get():
            self._process_exit(event.type)
            if func := events.get(event.type):
                func(event)

    def _set_background(self, image: pygame.Surface) -> None:
        screen_width, screen_height = self.screen.get_size()
        image_width, image_height = image.get_size()

        tiles_x = screen_width // image_width + 1
        tiles_y = screen_height // image_height + 1

        for x in range(tiles_x):
            for y in range(tiles_y):
                self.screen.blit(image, (image_width * x, image_height * y))

    def _loop(self, func: Callable, events: Mapping[int, Callable] = None) -> None:
        while True:
            if events is not None:
                self._process_events(events=events)
            func(self)
            pygame.display.flip()
            self.clock.tick(60)

    def init(self) -> None:
        pass

    def run(self) -> None:
        raise NotImplementedError()
