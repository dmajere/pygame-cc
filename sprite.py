from typing import Mapping
import pygame
from pathlib import Path
from random import randint

from common import Game, Asset

ASSETS_DIR = Path("assets/shooting-gallery-pack")


class Crosshair(Asset):
    def __init__(
        self, x: int, y: int, image: pygame.Surface, sound: pygame.mixer.Sound
    ) -> None:
        super().__init__(x, y, image)
        self.sound = sound

    def shoot(self, target):
        self.sound.play()
        pygame.sprite.spritecollide(self, target, True)

    def update(self):
        self.rect.center = pygame.mouse.get_pos()


class Target(Asset):
    def __init__(self, x: int, y: int, image: pygame.Surface) -> None:
        super().__init__(x, y, image, scale=(50, 50))


class ShootingRange(Game):
    TARGET_COUNT: int = 10

    def __init__(
        self,
        screen_width: int,
        screen_height: int,
        images: Mapping[str, Path] = None,
        sounds: Mapping[str, Path] = None,
    ):
        super().__init__(screen_width, screen_height, images=images, sounds=sounds)
        self.stage = "intro"

    def init(self):
        self.player = Crosshair(0, 0, self.images.crosshair, self.sounds.shot)
        self.player_group = pygame.sprite.Group()
        self.player_group.add(self.player)
        self.target_group = None

    def set_stage(self, stage: str) -> str:
        self.stage = stage

    def intro(self) -> None:
        def _start_game(_: pygame.event.Event):
            self.player.sound.play()
            self.set_stage("main")

        events = {
            pygame.MOUSEBUTTONDOWN: _start_game,
        }
        self._process_events(events)

        self._set_background(self.images.background)
        coordinates = (
            self.screen.get_width() / 2 - self.images.ready.get_width() / 2,
            self.screen.get_height() / 2 - self.images.ready.get_height() / 2,
        )
        self.screen.blit(self.images.ready, coordinates)

        self.player_group.draw(self.screen)
        self.player_group.update()

    def main(self) -> None:
        # if self.target_group is None:
        if not self.target_group:
            target_width = 50
            target_height = 50

            self.target_group = pygame.sprite.Group()
            for t in range(self.TARGET_COUNT):
                x = randint(
                    target_width / 2, self.screen.get_width() - target_width / 2
                )
                y = randint(
                    target_height / 2, self.screen.get_height() - target_height / 2
                )
                t = Target(x, y, self.images.target)
                self.target_group.add(t)

        events = {
            pygame.MOUSEBUTTONDOWN: lambda _: self.player.shoot(self.target_group),
        }
        self._process_events(events)

        self._set_background(self.images.background)
        self.target_group.draw(self.screen)

        self.player_group.draw(self.screen)
        self.player_group.update()

    def run(self) -> None:
        def _run(self) -> None:
            if self.stage == "intro":
                self.intro()
            elif self.stage == "main":
                self.main()

        self._loop(_run)


screen_width = 800
screen_height = 600
images = {
    "background": ASSETS_DIR / "PNG" / "Stall" / "bg_blue.png",
    "ready": ASSETS_DIR / "PNG" / "HUD" / "text_ready.png",
    "crosshair": ASSETS_DIR / "PNG" / "HUD" / "crosshair_red_small.png",
    "target": ASSETS_DIR / "PNG" / "Objects" / "target_red1.png",
}
sounds = {
    "shot": ASSETS_DIR / "Sounds" / "shot.wav",
}
game = ShootingRange(
    screen_width=screen_width,
    screen_height=screen_height,
    images=images,
    sounds=sounds,
)
game.run()
