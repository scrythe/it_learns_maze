import neat
from pygame import rect, key
import pygame
import math

import game


class Player:
    speed = 4
    fov = 45
    rays_amount = 5

    def __init__(
        self,
        pos: tuple[int, int],
        radius: int,
        boxes: list[pygame.Rect],
        boxes_type: list[bool],
        path_cells: list[pygame.Rect],
        genome,
        net: neat.nn.FeedForwardNetwork,
        maze_width: int,
        cell_width: int,
        best_genome: bool,
    ) -> None:
        self.image = pygame.Surface((radius * 2, radius * 2))
        self.rect: rect.FRect = self.image.get_frect(center=pos)
        self.boxes = boxes
        self.boxes_type = boxes_type
        self.path_cells = path_cells
        self.path_cells_score: list[int] = [0] * len(self.path_cells)
        self.genome = genome
        self.net = net
        self.best_genome = best_genome

        self.maze_width = maze_width
        self.cell_width = cell_width
        self.maze_inside_width = maze_width - cell_width * 2

        self.won = False

        self.image.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.image, "Red", (radius, radius), radius)

        self.direction = pygame.Vector2()
        self.angle = 0
        self.angle_direction = pygame.Vector2()
        self.rays: tuple[float, list[tuple[float, float, float, bool]]] = (0, [])

    def wasd_input(self):
        keys = key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        if self.direction:
            self.direction = self.direction.normalize()

    def angle_input(self):
        keys = key.get_pressed()
        # self.get_ai_input_data()
        self.angle += (keys[pygame.K_d] - keys[pygame.K_a]) / 10
        if self.angle < 0:
            self.angle += 2 * math.pi
        if self.angle > 2 * math.pi:
            self.angle -= 2 * math.pi
        direction = keys[pygame.K_w] - keys[pygame.K_s]
        self.angle_direction.x = math.cos(self.angle)
        self.angle_direction.y = math.sin(self.angle)
        self.direction.x = self.angle_direction.x * direction
        self.direction.y = self.angle_direction.y * direction

    def get_ai_input_data(self):
        inputs = [self.rays[0]]
        normalised_x = (self.rect.x - self.cell_width) / (
            self.maze_inside_width - self.rect.width
        )
        normalised_y = (
            self.rect.y - self.cell_width
        ) / self.maze_inside_width - self.rect.width
        inputs.append(normalised_x)
        inputs.append(normalised_y)
        for ray in self.rays[1]:
            normalised_ray = ray[2] / (
                self.maze_inside_width
            )  # when diagonal potentialn to still be above 1
            inputs.append(normalised_ray)
        return inputs

    def ai_input(self):
        inputs = self.get_ai_input_data()
        output = self.net.activate(inputs)
        angle_out = (output[0] - output[1]) / 60
        angle_out = max(angle_out, -1)
        self.angle += min(angle_out, 1)
        if self.angle < 0:
            self.angle += 2 * math.pi
        if self.angle > 2 * math.pi:
            self.angle -= 2 * math.pi
        direction = (output[2]) / 60
        direction = min(direction, 1.0)
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
                self.genome.fitness += 100
            collided_rect = self.boxes[collision_index]
            self.genome.fitness -= 0.05
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

    def path_collision(self):
        collision_index = self.rect.collidelist(self.path_cells)
        if collision_index != -1:
            self.path_cells_score[collision_index] += 1

    def calculate_fitness(self):
        fitness = 0
        for score in self.path_cells_score:
            if score > 250:
                fitness -= score / 10
            elif score > 0:
                fitness += 1 / score * 100
        self.genome.fitness += fitness

    def update(self, maze):
        self.raycasting(maze)
        self.ai_input()
        # self.angle_input()
        self.move()
        self.path_collision()

    def draw_rays(self, screen: pygame.Surface):
        rays = self.rays[1]
        for ray in rays:
            if ray[3]:
                pygame.draw.line(screen, "Blue", self.rect.center, (ray[0], ray[1]), 2)
            else:
                pygame.draw.line(screen, "Green", self.rect.center, (ray[0], ray[1]), 2)

    def draw_look_direction(self, screen: pygame.Surface):
        end_line_x = self.rect.centerx + self.angle_direction.x * 20
        end_line_y = self.rect.centery + self.angle_direction.y * 20
        pygame.draw.line(screen, "Blue", self.rect.center, (end_line_x, end_line_y), 2)

    def draw(self, screen: pygame.Surface):
        self.draw_look_direction(screen)
        if self.best_genome:
            self.draw_rays(screen)
            self.draw_3D(screen)
        screen.blit(self.image, self.rect)

    def draw_3D(self, screen: pygame.Surface):
        line_width = int(self.maze_width / self.rays_amount)
        current_x = self.maze_width + line_width / 2
        rays = self.rays[1]
        for ray in rays:
            length = self.maze_width / ray[2] * self.cell_width
            length = min(length, self.maze_width)
            if ray[3]:
                pygame.draw.line(
                    screen,
                    "Blue",
                    (current_x, self.maze_width / 2 - length / 2),
                    (current_x, self.maze_width / 2 + length / 2),
                    line_width,
                )
            else:
                pygame.draw.line(
                    screen,
                    "Green",
                    (current_x, self.maze_width / 2 - length / 2),
                    (current_x, self.maze_width / 2 + length / 2),
                    line_width,
                )
            current_x += line_width
