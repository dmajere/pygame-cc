import pygame
from typing import Tuple, Dict, Collection
from .types import Color


class Static(pygame.sprite.Sprite):
    def __init__(self, images: Dict[str, pygame.Surface], state: str) -> None:
        super().__init__()
        self._images = images
        self.rect = None
        self._load_state(state)

    def _load_state(self, state: str) -> None:
        self._state = state
        self.image = self._images[state]
        topleft = self.rect.topleft if self.rect else (0, 0)
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft
        self.mask = pygame.mask.from_surface(self.image)

    def set_state(self, state: str) -> None:
        self._load_state(state)


class Animated(pygame.sprite.Sprite):
    def __init__(
        self,
        animations: Dict[str, Tuple[Collection[pygame.Surface], float]],
        start_animation: str,
        start_frame: int = 0,
    ) -> None:
        super().__init__()
        self._is_running_animation = False
        self._animations = animations
        self._load_animation(start_animation, start_frame)

    def _reload_asset(self) -> None:
        self.image = self._animations[self._current_animation][0][self._current_frame]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def _load_animation(self, animation: str, start_frame: int) -> None:
        self._current_animation = animation
        self._current_rate = self._animations[self._current_animation][1]
        self._current_frame = start_frame
        self._reload_asset()

    def _animate(self):
        self._current_frame += self._current_rate
        frames = self._animations[self._current_animation][0]
        if self._current_frame >= len(frames):
            self._current_frame = 0
        self._reload_asset()
        if self._current_frame == 0:
            self._is_running_animation = False

    def update(self):
        if self._is_running_animation:
            self._animate()

    def start_animation(self, animation: str, start_frame: int = 0) -> None:
        self._is_running_animation = True
        self._load_animation(animation, start_frame)


class Text(pygame.sprite.Sprite):
    def __init__(
        self,
        text: str,
        font: pygame.font.Font,
        color: Color = "black",
        background: Color = None,
    ) -> None:
        super().__init__()
        self.image = font.render(text, False, color, background)
        self.rect = self.image.get_rect()
