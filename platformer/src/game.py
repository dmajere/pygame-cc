import pygame
import sys
from typing import Dict
from settings import SCREEN_HEIGHT, SCREEN_WIDHT
from level import Level
from pytmx.util_pygame import load_pygame
from pytmx import TiledMap
from pathlib import Path


class Game:
    FRAME_RATE: int = 120

    def __init__(self) -> None:
        pygame.init()
        self.display = pygame.display.set_mode((SCREEN_WIDHT, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Super Pirate World")

        self.tmx_maps = self.load_tmx_maps()
        self.current_stage = Level(self.tmx_maps["omni"])

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

    def quit(self) -> None:
        pygame.quit()
        sys.exit()

    def load_tmx_maps(self) -> Dict[str, TiledMap]:
        tmx_dir = Path("../data/levels")
        return {
            ppath.name[:-4]: load_pygame(ppath)
            for ppath in tmx_dir.iterdir()
            if ppath.name.endswith(".tmx")
        }

    def run(self) -> None:
        while True:
            dt = self.clock.tick(self.FRAME_RATE) / 1000
            self.process_events()

            self.current_stage.draw(self.display, dt)

            pygame.display.update()
