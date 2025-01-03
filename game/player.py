from pygame import rect, key
import pygame
import math

import game


class Player:
    speed = 4

    def __init__(
        self,
        pos: tuple[int, int],
        radius: int,
        walls: list[pygame.Rect],
    ) -> None:
        self.image = pygame.Surface((radius * 2, radius * 2))
        self.rect: rect.FRect = self.image.get_frect(center=pos)
        self.walls = walls

        self.image.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.image, "Red", (radius, radius), radius)

        self.direction = pygame.Vector2()
        self.angle = 0
        self.angle = 3 / 2 * math.pi
        self.angle_direction = pygame.Vector2()
        self.ray = (0, 0)

    def input(self):
        keys = key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        if self.direction:
            self.direction = self.direction.normalize()

    def input2(self):
        keys = key.get_pressed()
        self.angle += (keys[pygame.K_d] - keys[pygame.K_a]) / 20
        if self.angle < 0:
            self.angle += 2 * math.pi
        if self.angle > 2 * math.pi:
            self.angle -= 2 * math.pi
        direction = keys[pygame.K_w] - keys[pygame.K_s]
        self.angle_direction.x = math.cos(self.angle)
        self.angle_direction.y = math.sin(self.angle)
        self.direction.x = self.angle_direction.x * direction
        self.direction.y = self.angle_direction.y * direction

    def raycast(self, maze):
        self.ray = game.raycast(maze, self)

    def move(self):
        self.rect.x += self.direction.x * self.speed
        self.collision(True)
        self.rect.y += self.direction.y * self.speed
        self.collision(False)

    def collision(self, x_direction: bool):
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

    def update(self, maze):
        # self.input()
        self.input2()
        self.move()
        self.raycast(maze)

    def draw(self, screen: pygame.Surface):
        end_line_x = self.rect.centerx + self.angle_direction.x * 20
        end_line_y = self.rect.centery + self.angle_direction.y * 20
        pygame.draw.line(screen, "Blue", self.rect.center, (end_line_x, end_line_y), 2)
        pygame.draw.line(screen, "Green", self.rect.center, self.ray, 2)
        screen.blit(self.image, self.rect)
