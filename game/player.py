from pygame import sprite, rect, key
import pygame


class Player(sprite.Sprite):
    speed = 4

    def __init__(
        self,
        pos,
        radius,
        group: sprite.Group,
        walls: list[pygame.Rect],
    ) -> None:
        super().__init__(group)
        self.image = pygame.Surface((radius * 2, radius * 2))
        self.rect: rect.FRect = self.image.get_frect(center=pos)
        self.walls = walls

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
        self.collision(True)
        self.rect.y += self.direction.y * self.speed
        self.collision(False)

    def collision(self, x_direction):
        collision_index = self.rect.collidelist(self.walls)
        if collision_index != -1:
            collided_rect = self.walls[collision_index]
            if x_direction:
                if self.direction.x > 0:
                    self.rect.right = collided_rect.left
                else:
                    self.rect.left = collided_rect.right
            else:
                if self.direction.y > 0:
                    self.rect.bottom = collided_rect.top
                else:
                    self.rect.top = collided_rect.bottom

    def update(self):
        self.input()
        self.move()
