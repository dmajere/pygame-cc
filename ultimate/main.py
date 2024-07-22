import pygame
from typing import Dict, Tuple, Callable
from enum import IntEnum
from lib.asset import Static, Text
from lib.game import Game
from lib.types import AttrDict, Coordinate
from functools import cache
from monster import Snail
from player import Player
from lib.healthbar import HealthBar
from lib.scorebar import ScoreBar

SPRITESHEET_BG = (94, 129, 162)

"""
TODO:
* Start menu
* Stage return value
"""


class Background(IntEnum):
    SKY = 0
    FOREST = 1
    CAVE = 2


class Shape(IntEnum):
    DOT = 0
    BLOCK = 1
    # LSHAPE= 2
    # RLSHAPE= 3


class TerrainType(IntEnum):
    SAND = 0
    SNOW = 1
    GRASS = 2


_even = lambda x: x * 2
_odd = lambda x: x * 2 + 1

TILE_START_AT: Coordinate = (3, 3)
TILE_MARGIN: Coordinate = (2, 2)
TILE_SIZE: Tuple[int, int] = (21, 21)
TILES_FRAMES: Dict[str, Tuple[Callable, int]] = {
    "dot": (1, _even),
    "sharp_top": (3, _even),
    "sharp_bottom": (2, _odd),
}


class Ultimate(Game):

    STAGES = [
        AttrDict(
            {
                "background": Background.SKY,
                "terrain": TerrainType.GRASS,
            }
        ),
    ]

    def init(self) -> None:
        self.ground = pygame.sprite.GroupSingle(self.get_ground_block())

        game_font = pygame.font.Font(None, 50)
        self.game_over = pygame.sprite.GroupSingle(
            Text(
                "Game Over",
                game_font,
                (255, 204, 1),
                (208, 244, 247),
            )
        )
        self.game_over.sprite.rect.center = (self.screen.get_width() // 2, 50)

        self.player = pygame.sprite.GroupSingle(self.make_player())
        self.healthbar = HealthBar(
            75, 20, (215, 29, 29), icon=self.get_from_spritesheet(19, 4)
        )
        self.scorebar = ScoreBar(
            40,
            40,
            [self.get_from_spritesheet(pos_x, 6) for pos_x in range(20, 30)],
        )
        self.monster_group = pygame.sprite.Group()

        self.snail = self.make_snail(self.player.sprite, self.scorebar)
        self.monster_group.add(self.snail)

    def get_background(self, bg: Background) -> pygame.Surface:
        background_width: int = 231
        background_height: int = 63
        return pygame.transform.scale(
            self.get_image(
                self.images.backgrounds,
                size=(background_width, background_height),
                frame=(0, bg.value),
            ),
            (self.screen.get_width(), self.screen.get_height()),
        )

    def get_ground_block(self) -> Static:
        block_width = self.screen.get_width() // TILE_SIZE[0] + 1
        ground_height = int(self.screen.get_height() * 0.15)  # 15% is taken by ground
        block_height = ground_height // TILE_SIZE[1] + 1

        ground_images = {
            str(terrain_type): self.get_platform(
                block_width, block_height, Shape.BLOCK, terrain_type
            )
            for terrain_type in TerrainType
        }
        ground = Static(ground_images, "0")
        return ground

    def get_platform(
        self, width: int, height: int, shape: Shape, terrain_type: TerrainType
    ) -> pygame.Surface:
        terrain_tiles = self._get_terrain_tiles(terrain_type)
        return self._draw_shape(width, height, shape, terrain_tiles)

    def make_snail(self, player, score) -> Snail:
        snail_images = {
            Snail.State.RUN.value: pygame.transform.scale(
                self.get_from_spritesheet(14, 15), (60, 60)
            ),
            Snail.State.HATCHED.value: pygame.transform.scale(
                self.get_from_spritesheet(15, 15), (60, 60)
            ),
            Snail.State.DEAD.value: pygame.transform.scale(
                self.get_from_spritesheet(16, 15), (60, 60)
            ),
        }
        return Snail(player, score, snail_images, Snail.State.RUN, speed=(-3, 0))

    def make_player(self) -> Player:
        player_images = {
            str(value): pygame.transform.scale(
                self.get_from_spritesheet(value, 0), (70, 70)
            )
            for value in Player.State
        }
        return Player(player_images, str(Player.State.IDLE))

    def get_from_spritesheet(self, x: int, y: int) -> pygame.Surface:
        return self.get_image(
            self.images.spritesheet,
            size=TILE_SIZE,
            frame=(x, y),
            start_at=TILE_START_AT,
            margin=TILE_MARGIN,
            color=SPRITESHEET_BG,
        ).convert_alpha()

    @cache
    def _get_terrain_tiles(
        self, terrain_type: TerrainType
    ) -> Dict[str, pygame.Surface]:
        return {
            key: self.get_from_spritesheet(value[0], value[1](terrain_type.value))
            for key, value in TILES_FRAMES.items()
        }

    def _draw_shape(
        self,
        width: int,
        height: int,
        shape: Shape,
        terrain_tiles: Dict[str, pygame.Surface],
    ) -> pygame.Surface:
        if shape == shape.DOT:
            return terrain_tiles["dot"]
        elif shape == shape.BLOCK:
            block = pygame.Surface(
                (width * TILE_SIZE[0], height * TILE_SIZE[1])
            ).convert_alpha()
            for row in range(height):
                for col in range(width):
                    pos_x = col * TILE_SIZE[0]
                    pos_y = row * TILE_SIZE[1]
                    tile = (
                        terrain_tiles["sharp_top"]
                        if row == 0
                        else terrain_tiles["sharp_bottom"]
                    )
                    block.blit(tile, (pos_x, pos_y))
            return block

    def run(self) -> None:
        STAGE = 0
        stage_config: AttrDict = self.STAGES[STAGE]

        background = self.get_background(stage_config.background)

        ground_pos_y = self.screen.get_height() - self.ground.sprite.rect.height

        self.ground.sprite.rect.topleft = (0, ground_pos_y)
        self.ground.sprite.set_state(str(stage_config.terrain))
        self.snail.start_at(self.ground.sprite.rect.topright)

        self.player.sprite.rect.bottomleft = (20, ground_pos_y)
        self.player.sprite.ground = self.ground

        self.spawn = 0

        def _game_over(self) -> None:
            self.screen.fill((255, 0, 0))
            self.game_over.draw(self.screen)
            return True

        def _hb_test(self) -> None:
            self.screen.fill(SPRITESHEET_BG)
            self.scorebar.draw(self.screen, (self.screen.get_width() - 50, 30))
            return True

        def _run(self) -> None:
            if self.spawn >= 27000:
                self.spawn = 0
                self.monster_group.add(self.snail)
                self.snail.start_at(self.ground.sprite.rect.topright)
            self.spawn += 60

            self.screen.blit(background, (0, 0))

            # self.screen.blit(self.title, (300, 50))
            self.ground.draw(self.screen)
            self.healthbar.draw(self.screen, (50, 30))
            self.scorebar.draw(self.screen, (self.screen.get_width() - 50, 30))

            self.player.draw(self.screen)
            self.monster_group.draw(self.screen)

            self.player.update()
            self.monster_group.update()
            self.healthbar.set_health(self.player.sprite.get_health())

            if self.player.sprite.health <= 0:
                return False
            return True

        events = {
            pygame.KEYDOWN: self.player.sprite.action,
        }
        self.loop(_run, events=events)
        self.loop(_game_over, events={})


screen_width = 800
screen_height = 600
images = {
    "spritesheet": "assets/spritesheet.png",
    "backgrounds": "assets/backgrounds.png",
}
game = Ultimate(screen_width, screen_height, images=images)
game.run()
