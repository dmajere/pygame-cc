import sys
import pygame
from typing import Dict, Tuple, Callable
from enum import IntEnum
from lib.asset import Static, Text
from lib.game import Game
from lib.types import AttrDict, Coordinate
from functools import cache
from monster import Snail, Fly
from player import Player
from lib.healthbar import HealthBar
from lib.scorebar import ScoreBar
from lib.button import Button
from lib.timer import Timer

SPRITESHEET_BG = (94, 129, 162)


class GameOver(Exception):
    pass


"""
TODO:
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
    char_height = 50
    text_color = (255, 204, 1)
    button_color = ((94, 129, 162),)

    start_game_button = None
    retry_game_button = None
    exit_game_button = None

    stage = None
    session_start_time = 0
    timers = []

    STAGES = [
        AttrDict(
            {
                "background": Background.SKY,
                "terrain": TerrainType.GRASS,
            }
        ),
    ]

    def init(self) -> None:
        self.game_font = pygame.font.Font(None, self.char_height)
        self.init_buttons()
        self.init_hud()

        self.ground = pygame.sprite.GroupSingle(self.get_ground_block())
        self.player = pygame.sprite.GroupSingle(self.make_player())

        self.monster_group = pygame.sprite.Group()
        self.timers.append(
            Timer(
                self.spawn_snail,
                second=2,
            )
        )
        self.timers.append(
            Timer(
                self.spawn_fly,
                second=3,
            )
        )

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

    def start_timers(self) -> None:
        [t.start() for t in self.timers]

    def tick_timers(self) -> None:
        [t.tick() for t in self.timers]

    def stop_timers(self) -> None:
        [t.stop() for t in self.timers]

    def spawn_snail(self) -> None:
        snail = self.make_snail(self.player.sprite, self.scorebar)
        snail.start_at(self.ground.sprite.rect.topright)
        self.monster_group.add(snail)

    def make_snail(self, player, score) -> Snail:
        snail_images = {
            Snail.State.RUN1.value: pygame.transform.scale(
                self.get_from_spritesheet(13, 15), (60, 60)
            ),
            Snail.State.RUN2.value: pygame.transform.scale(
                self.get_from_spritesheet(14, 15), (60, 60)
            ),
            Snail.State.HATCHED.value: pygame.transform.scale(
                self.get_from_spritesheet(15, 15), (60, 60)
            ),
            Snail.State.DEAD.value: pygame.transform.scale(
                self.get_from_spritesheet(16, 15), (60, 60)
            ),
        }
        return Snail(player, score, snail_images, Snail.State.RUN1, speed=(-3, 0))

    def spawn_fly(self) -> None:
        fly = self.make_fly(self.player.sprite, self.scorebar)
        x, y = self.ground.sprite.rect.topright
        fly.start_at((x, y - 20))
        self.monster_group.add(fly)

    def make_fly(self, player, score) -> Fly:
        fly_images = {
            Snail.State.RUN1.value: pygame.transform.scale(
                self.get_from_spritesheet(13, 14), (60, 60)
            ),
            Snail.State.RUN2.value: pygame.transform.scale(
                self.get_from_spritesheet(14, 14), (60, 60)
            ),
            Snail.State.DEAD.value: pygame.transform.scale(
                self.get_from_spritesheet(15, 14), (60, 60)
            ),
        }
        return Fly(
            player,
            score,
            fly_images,
            Fly.State.RUN1,
            speed=(-5, 0),
            run_animation_speed=5,
        )

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

    def start_game(self):
        self.stage = 0

    def init_buttons(self):
        if not self.start_game_button:
            start_game_text = Text("Start Game", self.game_font, self.text_color)
            self.start_game_button = Button(
                self.button_color,
                onClick=self.start_game,
                margin=8,
                border_width=2,
                border_radius=10,
                border_color="darkblue",
                text=start_game_text,
            )
        if not self.exit_game_button:
            exit_game_text = Text("Exit", self.game_font, self.text_color)
            self.exit_game_button = Button(
                self.button_color,
                onClick=self.exit,
                width=self.start_game_button.rect.width,
                height=self.start_game_button.rect.height,
                border_width=2,
                border_radius=10,
                border_color="darkblue",
                text=exit_game_text,
            )
        if not self.retry_game_button:
            retry_text = Text("Retry?", self.game_font, self.text_color)
            self.retry_game_button = Button(
                self.button_color,
                onClick=self.start_game,
                width=self.start_game_button.rect.width,
                height=self.start_game_button.rect.height,
                border_width=2,
                border_radius=10,
                border_color="darkblue",
                text=retry_text,
            )

    def init_hud(self) -> None:
        self.healthbar = HealthBar(
            75, 20, (215, 29, 29), icon=self.get_from_spritesheet(19, 4)
        )
        self.scorebar = ScoreBar(
            40,
            40,
            [self.get_from_spritesheet(pos_x, 6) for pos_x in range(20, 30)],
        )
        self.game_over = pygame.sprite.GroupSingle(
            Text(
                "Game Over",
                self.game_font,
                self.text_color,
                self.button_color,
            )
        )
        self.game_over.sprite.rect.center = (self.screen.get_width() // 2, 50)

    def run_game_menu(self) -> None:
        background = self.get_background(Background.SKY)

        def _process_event(event: pygame.event.Event):
            self.start_game_button.process_event(event)
            self.exit_game_button.process_event(event)

        def _run_menu(self) -> bool:
            if self.stage is not None:
                return False
            self.screen.blit(background, (0, 0))
            pygame.mouse.set_visible(True)

            self.start_game_button.draw(self.screen, (400, 200))
            self.exit_game_button.draw(self.screen, (400, 300))
            return True

        events = {
            pygame.MOUSEBUTTONDOWN: _process_event,
        }
        self.loop(_run_menu, events=events)

    def run_stage(self, stage: int) -> None:
        stage_config: AttrDict = self.STAGES[stage]

        background = self.get_background(stage_config.background)

        ground_pos_y = self.screen.get_height() - self.ground.sprite.rect.height
        self.ground.sprite.rect.topleft = (0, ground_pos_y)
        self.ground.sprite.set_state(str(stage_config.terrain))

        self.player.sprite.rect.bottomleft = (20, ground_pos_y)
        self.player.sprite.ground = self.ground

        self.start_timers()

        def _run(self) -> None:
            self.tick_timers()

            self.screen.blit(background, (0, 0))

            self.ground.draw(self.screen)
            self.healthbar.draw(self.screen, (50, 30))
            self.scorebar.draw(self.screen, (self.screen.get_width() - 50, 30))

            self.player.draw(self.screen)
            self.monster_group.draw(self.screen)

            self.player.update()
            self.monster_group.update()
            self.healthbar.set_health(self.player.sprite.get_health())

            if self.player.sprite.health <= 0:
                self.stop_timers()
                raise GameOver()
            return True

        events = {
            pygame.KEYDOWN: self.player.sprite.action,
        }
        self.loop(_run, events=events)

    def run_game_over(self) -> None:
        background = self.get_background(Background.SKY)
        self.stage = None

        def _process_event(event: pygame.event.Event):
            self.retry_game_button.process_event(event)
            self.exit_game_button.process_event(event)

        def _run_game_over(self) -> bool:
            if self.stage is not None:
                return False

            self.screen.blit(background, (0, 0))
            pygame.mouse.set_visible(True)

            self.game_over.draw(self.screen)

            self.retry_game_button.draw(self.screen, (400, 200))
            self.exit_game_button.draw(self.screen, (400, 300))
            return True

        self.loop(
            _run_game_over,
            events={
                pygame.MOUSEBUTTONDOWN: _process_event,
            },
        )

    def run(self) -> None:
        self.run_game_menu()
        while True:
            self.player.sprite.health = 100
            try:
                self.run_stage(self.stage)
            except GameOver:
                self.run_game_over()


screen_width = 800
screen_height = 600
images = {
    "spritesheet": "assets/spritesheet.png",
    "backgrounds": "assets/backgrounds.png",
}
game = Ultimate(screen_width, screen_height, images=images)
game.run()
