import pygame
from common import Game, Masked


class Player(Masked):
    def update(self):
        self.rect.center = pygame.mouse.get_pos()


class Obstacle(Masked):
    pass


class Masks(Game):
    def init(self) -> None:
        ps = pygame.Surface((20, 20))
        ps.fill((255, 0, 0))
        self.player = Player(0, 0, ps)
        self.player_group = pygame.sprite.GroupSingle(self.player)

        self.obstacle = Obstacle(
            self.screen.get_width() / 2, self.screen.get_height() / 2, self.images.duck
        )
        self.obstacle_group = pygame.sprite.GroupSingle(self.obstacle)

    def run(self) -> None:
        def _run(self) -> None:
            self.screen.fill((255, 255, 255))
            self.player_group.draw(self.screen)
            self.obstacle_group.draw(self.screen)
            self.player_group.update()

            offset_x = self.obstacle.rect.topleft[0] - self.player.rect.left
            offset_y = self.obstacle.rect.topleft[1] - self.player.rect.top
            if self.player.mask.overlap(self.obstacle.mask, (offset_x, offset_y)):
                overlap_mask = self.player.mask.overlap_mask(
                    self.obstacle.mask, (offset_x, offset_y)
                )
                shadowed = self.player.make_shadowed(overlap_mask, "lightblue")
                self.screen.blit(shadowed, self.player.rect)

        #            if pygame.sprite.spritecollide(
        #                self.player,
        #                self.obstacle_group,
        #                False,
        #            ):
        #                if collisions := pygame.sprite.spritecollide(
        #                    self.player,
        #                    self.obstacle_group,
        #                    False,
        #                    collided=pygame.sprite.collide_mask,
        #                ):
        #                    self.player.image.fill((0, 255, 0))
        #            else:
        #                self.player.image.fill((255, 0, 0))

        events = {}
        self._loop(_run, events=events)


images = {
    "duck": "assets/shooting/duck_yellow.png",
}
game = Masks(600, 600, images=images)
game.run()
