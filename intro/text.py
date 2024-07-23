import pygame
from common import Game, TextBox


class Text(Game):
    def init(self) -> None:
        self.textbox = TextBox(200, 200, 140, 32, default_text="Input")
        pygame.mouse.set_visible(True)

    def run(self) -> None:
        events = {
            pygame.MOUSEBUTTONDOWN: self.textbox.toggle,
            pygame.KEYDOWN: self.textbox.input,
        }

        def _run(self) -> None:
            self.screen.fill((0, 0, 0))
            self.textbox.draw(self.screen)

        self._loop(
            _run,
            events=events,
        )


images = {}

rotate = Text(500, 500, images=images)
rotate.run()
