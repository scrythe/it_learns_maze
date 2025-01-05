from pygame import rect, key
import pygame
import math

import game


class Player:
    speed = 4
    fov = 30
    rays_amount = 30

    def __init__(
        self,
        pos: tuple[int, int],
        radius: int,
        boxes: list[pygame.Rect],
        boxes_type: list[bool],
    ) -> None:
        self.image = pygame.Surface((radius * 2, radius * 2))
        self.rect: rect.FRect = self.image.get_frect(center=pos)
        self.boxes = boxes
        self.boxes_type = boxes_type
        self.won = False

        self.image.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.image, "Red", (radius, radius), radius)

        self.direction = pygame.Vector2()
        self.angle = 0
        self.angle_direction = pygame.Vector2()
        self.rays: list[tuple[float, float, float, bool]] = []

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

    def raycasting(self, maze):
        self.rays = game.raycasting(maze, self, self.fov, self.rays_amount)

    def move(self):
        self.rect.x += self.direction.x * self.speed
        self.collision(True)
        self.rect.y += self.direction.y * self.speed
        self.collision(False)

    def collision(self, x_direction: bool):
        collision_index = self.rect.collidelist(self.boxes)
        if collision_index != -1:
            collided_box_type = self.boxes_type[collision_index]
            if collided_box_type:
                self.won = True
            collided_rect = self.boxes[collision_index]
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
        self.input2()
        self.move()
        self.raycasting(maze)

    def draw_rays(self, screen: pygame.Surface):
        for ray in self.rays:
            if ray[3]:
                pygame.draw.line(screen, "Blue", self.rect.center, (ray[0], ray[1]), 2)
            else:
                pygame.draw.line(screen, "Green", self.rect.center, (ray[0], ray[1]), 2)

    def draw(self, screen: pygame.Surface):
        print(self.rect)
        screen.blit(self.image, self.rect)
        self.draw_rays(screen)

    def draw_3D(self, screen: pygame.Surface, box_size: int, cell_width: int):
        line_width = int(box_size / self.rays_amount)
        current_x = box_size + line_width / 2
        for ray in self.rays:
            length = box_size / ray[2] * cell_width
            length = min(length, box_size)
            if ray[3]:
                pygame.draw.line(
                    screen,
                    "Blue",
                    (current_x, box_size / 2 - length / 2),
                    (current_x, box_size / 2 + length / 2),
                    line_width,
                )
            else:
                pygame.draw.line(
                    screen,
                    "Green",
                    (current_x, box_size / 2 - length / 2),
                    (current_x, box_size / 2 + length / 2),
                    line_width,
                )
            current_x += line_width
