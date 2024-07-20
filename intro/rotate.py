from pathlib import Path
import pygame
from common import Game, Asset, Rotating


class Rotate(Game):
    angle = 0

    def init(self) -> None:
        self.duck = Rotating(100, 100, self.images.duck)
        self.duck_group = pygame.sprite.Group()
        self.duck_group.add(self.duck)

    def run(self) -> None:
        def _run(self) -> None:
            self.screen.fill((255, 255, 255))

            self.duck_group.draw(self.screen)
            self.duck_group.update()

        self._loop(_run, events={})


images = {
    "duck": "assets/shooting/duck_yellow.png",
}

rotate = Rotate(500, 500, images=images)
rotate.run()
