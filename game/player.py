from pygame import sprite, rect, key
import pygame


class Player(sprite.Sprite):
    speed = 5
    def __init__(
        self,
        pos,
        radius,
        group: sprite.Group,
        walls: sprite.Group,
    ) -> None:
        super().__init__(group)
        self.image = pygame.Surface((radius * 2, radius * 2))
        self.rect: rect.FRect = self.image.get_frect(center=pos)

        self.image.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.image, "Red", (radius, radius), radius)

        self.direction = pygame.Vector2()

    def input(self):
        keys = key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        if self.direction:
            self.direction = self.direction.normalize()

    def move(self):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

    def update(self):
        self.input()
        self.move()
