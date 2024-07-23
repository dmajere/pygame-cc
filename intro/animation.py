import pygame
from common import Game, Animation


class AnimationGame(Game):
    def init(self) -> None:
        image_names = sorted(self.images.keys())
        frames = [self.images[name] for name in image_names]
        self.player = Animation(100, 100, frames)

        self.player_group = pygame.sprite.Group()
        self.player_group.add(self.player)

    def run(self) -> None:
        def _run(self) -> None:
            self.screen.fill((0, 0, 0))
            self.player_group.draw(self.screen)
            self.player_group.update()

        events = {pygame.KEYDOWN: lambda _: self.player.trigger()}
        self._loop(_run, events=events)


images = {f"frog-0{idx}": f"assets/frog_attack/frame-0{idx}.gif" for idx in range(10)}

game = AnimationGame(
    800,
    600,
    images=images,
    caption="Sprite Animation",
)
game.run()
