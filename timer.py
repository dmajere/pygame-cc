import pygame
import sys

from common import Game, Timer


class TimerGame(Game):
    def init(self) -> None:
        self.timer = Timer(self.clock)

    def run(self) -> None:
        def trigger(_: pygame.event.Event) -> None:
            self.timer.trigger()
            self.screen.fill((255, 255, 255))

        events = {
            pygame.KEYDOWN: trigger,
        }

        def _run(self) -> None:
            if self.timer.is_expired:
                self.screen.fill((0, 0, 0))

        self._loop(_run, events=events)


game = TimerGame(200, 200)
game.run()
