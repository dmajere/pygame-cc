import sys
import pygame
from typing import Mapping, Callable, Tuple
from .types import AttrDict, Coordinate, Color


class Game:
    def __init__(
        self,
        screen_width: int,
        screen_height: int,
        images: Mapping[str, str] = None,
        sounds: Mapping[str, str] = None,
        mouse_visible: bool = False,
        caption: str = "",
        frame_rate: int = 60,
    ):
        self.frame_rate = frame_rate
        self.clock = pygame.time.Clock()
        pygame.init()
        pygame.mouse.set_visible(mouse_visible)
        self.screen = pygame.display.set_mode((screen_width, screen_height))

        self.images: AttrDict = (
            self._load_assets(images, pygame.image.load) if images else AttrDict()
        )
        self.images = AttrDict(
            {key: value.convert_alpha() for key, value in self.images.items()}
        )
        self.sounds: AttrDict = (
            self._load_assets(sounds, pygame.mixer.Sound) if sounds else AttrDict()
        )
        pygame.display.set_caption(caption)

        self.init()

    def _load_assets(self, assets: Mapping[str, str], load_func: Callable):
        loaded = AttrDict()
        for key, path in assets.items():
            loaded[key] = load_func(path)
        return loaded

    def exit(self) -> None:
        pygame.quit()
        sys.exit(0)

    def process_events(self, events: Mapping[int, Callable]) -> None:
        events = events or {}
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()
            if func := events.get(event.type):
                func(event)

    def set_background(self, image: pygame.Surface) -> None:
        screen_width, screen_height = self.screen.get_size()
        image_width, image_height = image.get_size()

        tiles_x = screen_width // image_width + 1
        tiles_y = screen_height // image_height + 1

        for x in range(tiles_x):
            for y in range(tiles_y):
                self.screen.blit(image, (image_width * x, image_height * y))

    def loop(self, func: Callable, events: Mapping[int, Callable] = None) -> None:
        events = events or {}
        run = True
        while run:
            self.process_events(events=events)
            run = func(self)
            pygame.display.flip()
            self.clock.tick(self.frame_rate)

    def get_image(
        self,
        sheet: pygame.Surface,
        size: Coordinate,
        frame: Coordinate,
        start_at: Coordinate = None,
        margin: Coordinate = None,
        scale_factor: Coordinate = None,
        color: Color = None,
    ) -> pygame.Surface:
        image = pygame.Surface(size).convert_alpha()
        start_at = start_at or (0, 0)
        margin = margin or (0, 0)

        x = start_at[0] + size[0] * frame[0] + margin[0] * frame[0]
        y = start_at[1] + size[1] * frame[1] + margin[1] * frame[1]
        image.blit(sheet, (0, 0), (x, y, *size))
        if scale_factor:
            scale = (size[0] * scale_factor[0], size[1] * scale_factor[1])
            image = pygame.transform.scale(image, scale)
        image.set_colorkey(color)
        return image

    def get_range(
        self,
        sheet: pygame.Surface,
        size: Coordinate,
        frame_range: Tuple[Coordinate, Coordinate],
        start_at: Coordinate = None,
        margin: Coordinate = None,
        scale_factor: Coordinate = None,
        color: Color = None,
    ) -> pygame.Surface:
        range_x = frame_range[0]
        range_y = frame_range[1]

        count_x = range_x[1] - range_x[0]
        count_y = range_y[1] - range_y[0]

        image = pygame.Surface((count_x * size[0], count_y * size[1])).convert_alpha()
        for x in range(*range_x):
            for y in range(*range_y):
                _x = x - range_x[0]
                pos_x = _x * size[0]
                _y = y - range_y[0]
                pos_y = _y * size[1]

                image.blit(
                    self.get_image(
                        sheet,
                        size=size,
                        frame=(x, y),
                        start_at=start_at,
                        margin=margin,
                        color=color,
                    ),
                    (pos_x, pos_y),
                )

        if scale_factor:
            scale = (
                count_x * size[0] * scale_factor[0],
                count_y * size[1] * scale_factor[1],
            )
            image = pygame.transform.scale(image, scale)
        return image

    def init(self) -> None:
        pass

    def run(self) -> None:
        raise NotImplementedError()
