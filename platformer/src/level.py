import pygame
from settings import TILE_SIZE
from sprite import Sprite
from player import Player
from pytmx import TiledMap


class Level:
    def __init__(self, map: TiledMap) -> None:
        self.diplay = pygame.display.get_surface()

        self.sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        self.setup(map)

    def setup(self, map: TiledMap) -> None:
        for x, y, surface in map.get_layer_by_name("Terrain").tiles():
            s = Sprite(
                (x * TILE_SIZE, y * TILE_SIZE),
                surface,
                self.sprites,
                self.collision_sprites,
            )
            self.sprites.add(s)

        for obj in map.get_layer_by_name("Objects"):
            if obj.name == "player":
                Player(
                    (obj.x, obj.y),
                    obj.image,
                    self.collision_sprites,
                    self.sprites,
                    self.player,
                )

    def draw(self, surface: pygame.Surface, dt: float) -> None:
        surface.fill("black")
        self.sprites.draw(surface)
        self.player.update(dt)
