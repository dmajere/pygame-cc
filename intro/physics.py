from typing import List, Tuple
import pymunk
import pygame
from common import Game, Physical, Color, Coordinate
from random import randint


class Physics(Game):
    gravity = 40
    balls_num = 10
    apple_radius = 18
    ball_radius = 15

    def init(self) -> None:
        self.space = pymunk.Space()
        self.space.gravity = (0, self.gravity)
        self.apple_group = pygame.sprite.Group()

        self.balls = []
        for _ in range(self.balls_num):
            self.balls.append(
                self.create_ball(
                    randint(
                        self.ball_radius, self.screen.get_width() - self.ball_radius
                    ),
                    randint(
                        self.ball_radius, self.screen.get_height() - self.ball_radius
                    ),
                )
            )

    def create_shape(
        self,
        x: int,
        y: int,
        radius: int,
        mass: float = 0,
        inertia: float = 0,
        body_type: int = pymunk.Body.DYNAMIC,
    ) -> pymunk.Shape:
        body = pymunk.body.Body(mass, inertia, body_type=body_type)
        body.position = (x, y)
        shape = pymunk.Circle(body, radius)
        self.space.add(body, shape)
        return shape

    def create_apple(self, c: Coordinate) -> None:
        apple = Physical(
            *c,
            self.apple_radius,
            self.images.apple,
            self.space,
            mass=1,
            inertia=100,
            scale=(50, 50),
        )
        self.apple_group.add(apple)

    def delete_apple(self) -> None:
        for apple in self.apple_group:
            if apple.rect.y >= self.screen.get_height():
                apple.kill()

    def create_ball(self, x: int, y: int) -> pymunk.Shape:
        return self.create_shape(x, y, self.ball_radius, body_type=pymunk.Body.STATIC)

    def draw_shapes(self, shapes: List[pymunk.Shape], color: Color) -> None:
        for shape in shapes:
            pygame.draw.circle(self.screen, color, shape.body.position, shape.radius)

    def run(self) -> None:
        def _run(self) -> None:
            self.screen.fill((255, 255, 255))
            pygame.mouse.set_visible(True)
            self.space.step(1 / 50)
            self.apple_group.draw(self.screen)
            self.draw_shapes(self.balls, (0, 0, 255))
            self.apple_group.update()
            self.delete_apple()

        events = {pygame.MOUSEBUTTONDOWN: lambda e: self.create_apple(e.pos)}

        self._loop(_run, events=events)


images = {"apple": "assets/apple.png"}

game = Physics(600, 600, images=images)
game.run()
