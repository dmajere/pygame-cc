import pygame
from lib.asset import Static
from enum import IntEnum
from itertools import cycle


class Player(Static):
    class State(IntEnum):
        IDLE = 19
        DUCK = 22
        LAND = 23
        JUMP = 26
        AIR = 27
        WALK1 = 28
        WALK2 = 29

    health: int = 100
    gravity = 0
    in_jump = False

    _walk_frames = cycle([State.WALK1, State.WALK2])
    _walk_speed = 20
    _current_frame = 0

    def _animate_walk(self) -> None:
        self._current_frame += 1
        if self._current_frame >= self._walk_speed:
            self._current_frame = 0
            self.set_state(str(self._walk_frames.__next__()))

    def action(self, event: pygame.event.Event) -> None:
        if event.key == pygame.K_SPACE:
            self.jump()

    def jump(self) -> None:
        if not self.in_jump:
            self.in_jump = True
            self.gravity = -20

    def update(self) -> None:
        # if pygame.sprite.collide_rect(self, self.ground.sprite):
        if self.rect.bottom < self.ground.sprite.rect.top:
            self.set_state(str(self.State.JUMP))
            self.gravity += 1
        elif self.rect.bottom > self.ground.sprite.rect.top:
            self.rect.bottomleft = (
                self.rect.bottomleft[0],
                self.ground.sprite.rect.topleft[1],
            )
            self.gravity = 0
            self.in_jump = False
        else:
            self._animate_walk()
        self.rect.y += self.gravity

    def take_damage(self, damage: int) -> None:
        self.health -= int(damage)

    def get_health(self) -> int:
        return self.health
