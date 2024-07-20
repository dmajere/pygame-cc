from typing import Tuple, Callable
import pygame
from common import Game, Asset


class Laser(Asset):
    speed = 1

    def __init__(
        self,
        x: int,
        y: int,
        distance: int,
        speed: int,
        image: pygame.Surface,
        scale: Tuple[int, int] = None,
    ) -> None:

        super().__init__(x, y, image=image, scale=scale)
        self.distance = distance
        self.speed = speed

    def update(self):
        if self.rect.x >= self.distance:
            self.kill()
        self.rect.x += self.speed


class Player(Asset):
    def __init__(
        self,
        x: int,
        y: int,
        shooting_group: pygame.sprite.Group,
        max_shooting_distance: int,
        image: pygame.Surface,
        laser_image: pygame.Surface,
        scale: Tuple[int, int] = None,
    ) -> None:
        super().__init__(x, y, image=image, scale=scale)
        self.max_shooting_distnace = max_shooting_distance
        self.shooting_group = shooting_group
        self.laser_image = pygame.transform.scale(laser_image, (30, 10))

    def shoot(self):
        laser = Laser(
            *self.rect.midright,
            self.max_shooting_distnace,
            5,
            self.laser_image,
        )
        self.shooting_group.add(laser)

    def update(self):
        self.rect.center = pygame.mouse.get_pos()


class Shooting(Game):
    def init(self):
        self.player_group = pygame.sprite.Group()
        self.shots_group = pygame.sprite.Group()
        self.player = Player(
            0,
            0,
            self.shots_group,
            self.screen.get_width(),
            self.images.player,
            self.images.laser,
        )
        self.player_group.add(self.player)

    def run(self):
        def _run(self):
            self.screen.fill((0, 0, 0))
            self.player_group.draw(self.screen)
            self.player_group.update()
            self.shots_group.draw(self.screen)
            self.shots_group.update()

        events = {pygame.MOUSEBUTTONDOWN: lambda _: self.player.shoot()}
        self._loop(_run, events=events)


images = {
    "player": "assets/space/player_ship.png",
    "laser": "assets/space/red_laser.png",
}
game = Shooting(800, 600, images=images)
game.run()
