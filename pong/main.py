import sys
import pygame

pygame.init()
clock = pygame.time.Clock()

screen_width = 400
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))


class Pad(pygame.sprite.Sprite):
    def __init__(self, size, center, ball, speed=3):
        super(Pad, self).__init__()
        self.width, self.height = size
        self.ball = ball
        self.speed = speed

        self.image = pygame.Surface(size, pygame.SRCALPHA, 32).convert_alpha()
        self.border = pygame.rect.Rect((0, 0), size)
        pygame.draw.rect(self.image, (255, 255, 255), self.border, 1)

        self.rect = self.image.get_rect(center=center)

    def ball_collide(self):
        return self.rect.top <= self.ball.rect.bottom

    def move(self):
        if keys := pygame.key.get_pressed():
            k_left = keys[pygame.K_LEFT]
            k_right = keys[pygame.K_RIGHT]
            k_space = keys[pygame.K_SPACE]
            if k_space and self.ball_collide():
                print("SERVE")
                self.ball.serve((0, -1))

            if k_left:
                self.rect.x = max(5, self.rect.x - self.speed)
            elif k_right:
                self.rect.x = min(400 - self.width - 5, self.rect.x + self.speed)

    def update(self):
        self.move()


class Ball(pygame.sprite.Sprite):
    def __init__(self, radius, center, speed=3):
        super(Ball, self).__init__()
        self.radius = radius
        self.speed = speed
        self.served = False
        self.vec = (0, 0)

        self.image = pygame.Surface(
            (2 * self.radius, 2 * self.radius), pygame.SRCALPHA, 32
        )
        self.circle = pygame.draw.circle(
            self.image, (255, 255, 255), (self.radius, self.radius), radius, width=1
        )
        self.rect = self.image.get_rect(center=center)

    def serve(self, vector):
        self.served = True
        self.vec = vector

    def update(self, player):
        if not self.served:
            self.rect.midbottom = player.rect.midtop
        self.rect.x += self.vec[0]
        self.rect.y += self.vec[1]


radius = 10
ball = pygame.sprite.GroupSingle(Ball(radius, (0, 0)))
player = pygame.sprite.GroupSingle(
    Pad(
        (50, 20),
        (200, 600 - 15),
        ball=ball.sprite,
    )
)


ball.update(player.sprite)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))
    player.draw(screen)
    ball.draw(screen)

    player.update()
    ball.update(player.sprite)

    pygame.display.flip()
    clock.tick(60)
