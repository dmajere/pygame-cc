import pygame
from lib.asset import Static
from enum import IntEnum


class Player(Static):
    class State(IntEnum):
        IDLE = 19
        DUCK = 22
        LAND = 23
        JUMP = 26
        AIR = 27
        WALK1 = 28
        WALK2 = 29

    health = 100
    gravity = 0
    in_jump = False

    def action(self, event: pygame.event.Event) -> None:
        print(event)
        if event.key == pygame.K_SPACE:
            self.jump()
        
    def jump(self) -> None:
        if not self.in_jump:
            self.in_jump = True
            self.gravity = -20
        
    def update(self) -> None:
        # if pygame.sprite.collide_rect(self, self.ground.sprite):
        if self.rect.bottom < self.ground.sprite.rect.top:
            self.gravity += 1
        elif self.rect.bottom > self.ground.sprite.rect.top:
            self.rect.bottomleft = (self.rect.bottomleft[0], self.ground.sprite.rect.topleft[1])
            self.gravity = 0
            self.in_jump = False
        self.rect.y += self.gravity

    def take_damage(self, damage: float) -> None:
        self.health -= damage
    