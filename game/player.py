import neat
from pygame import rect, key
import pygame
import math

from game.raycast import Raycaster


class Player:
    speed = 4
    fov = 180
    rays_amount = 6
    LIFE_TIME = 40
    three_d_rays_amount = 160

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
        self.alive_image = pygame.Surface((radius * 2, radius * 2))
        self.alive_image.fill("White")
        self.rect: rect.FRect = self.alive_image.get_frect(center=pos)

        self.boxes = boxes
        self.boxes_type = boxes_type
        self.path_cells = path_cells
        self.path_cells_score: list[int] = [0] * len(self.path_cells)
        self.genome = genome
        self.net = net
        self.best_genome = best_genome
        self.life_time = self.LIFE_TIME
        self.total_time = 0

        self.maze_width = maze_width
        self.cell_width = cell_width
        self.maze_inside_width = 840 - cell_width * 2

        self.alive_image.set_colorkey((255, 255, 255))
        self.dead_image = self.alive_image.copy()
        self.best_image = self.alive_image.copy()

        pygame.draw.circle(self.alive_image, "Red", (radius, radius), radius)
        pygame.draw.circle(self.dead_image, "Black", (radius, radius), radius)
        pygame.draw.circle(self.best_image, "#3eb9c1", (radius, radius), radius)

        self.direction = pygame.Vector2()
        self.angle = 0
        self.angle_direction = pygame.Vector2()
        self.rays: list[tuple[float, float, float, float, bool]] = []

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
        inputs = []
        for ray in self.rays:
            normalised_ray = ray[2] / (
                self.maze_inside_width
            )  # when diagonal, potential to still be above 1
            inputs.append(normalised_ray)
        return inputs

    def ai_input(self):
        inputs = self.get_ai_input_data()
        output = self.net.activate(inputs)
        self.angle -= 0.1  # left
        if max(output[0], 0):  # if below 0 then 0
            self.angle += 0.2  # right
        direction = 0
        if max(output[1], 0):  # if below 0 then 0
            direction = 1  # forward
        if self.angle < 0:
            self.angle += 2 * math.pi
        if self.angle > 2 * math.pi:
            self.angle -= 2 * math.pi
        self.angle_direction.x = math.cos(self.angle)
        self.angle_direction.y = math.sin(self.angle)
        self.direction.x = self.angle_direction.x * direction
        self.direction.y = self.angle_direction.y * direction

    def raycasting(self, maze):
        self.rays = Raycaster.raycasting(
            maze, self.rect, self.angle, self.fov, self.rays_amount
        )

    def move(self):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed
        self.collision()

    def collision(self):
        collision_index = self.rect.collidelist(self.boxes)
        if collision_index != -1:
            is_goal = self.boxes_type[collision_index]
            # Tod nach Berührung mit Zelle. Belohnung falls Ziel und Bestrafung falls Wand.
            if is_goal:
                self.genome.fitness += 10000
                self.genome.fitness -= self.total_time
            else:
                self.genome.fitness -= 65
            self.life_time = 0
            return

    def path_collision(self):
        collision_index = self.rect.collidelist(self.path_cells)
        if collision_index != -1:
            if self.path_cells_score[collision_index] == 0:  # new cell
                self.life_time += 20
                self.genome.fitness += 8
            self.path_cells_score[collision_index] += 1
            if self.path_cells_score[collision_index] > 50:
                self.life_time = 0
                self.genome.fitness -= 80

    def update(self, maze):
        self.raycasting(maze)
        self.ai_input()
        # self.angle_input()
        self.move()
        self.path_collision()
        self.life_time -= 1
        self.total_time += 1

    def draw_rays(self, screen: pygame.Surface):
        for ray in self.rays:
            if ray[4]:
                pygame.draw.line(screen, "Blue", self.rect.center, (ray[0], ray[1]), 2)
            else:
                pygame.draw.line(screen, "Green", self.rect.center, (ray[0], ray[1]), 2)

    def draw_look_direction(self, screen: pygame.Surface):
        end_line_x = self.rect.centerx + self.angle_direction.x * 20
        end_line_y = self.rect.centery + self.angle_direction.y * 20
        pygame.draw.line(screen, "Blue", self.rect.center, (end_line_x, end_line_y), 2)

    def normal_draw(self, screen: pygame.Surface):
        if not self.best_genome:
            self.draw_look_direction(screen)
            if self.life_time <= 0:
                screen.blit(self.dead_image, self.rect)
            else:
                screen.blit(self.alive_image, self.rect)

    # seperate to draw on top of other players
    def best_player_draw(self, screen: pygame.Surface, maze):
        self.draw_look_direction(screen)
        self.draw_rays(screen)
        self.draw_3D(screen, maze)
        self.ai_view(screen, maze)
        screen.blit(self.best_image, self.rect)

    def draw_3D(self, screen: pygame.Surface, maze):
        line_width = self.maze_width * 2 / self.three_d_rays_amount
        current_x = line_width / 2
        rays = Raycaster.raycasting(
            maze, self.rect, self.angle, 90, self.three_d_rays_amount
        )
        for ray in rays:
            length = self.maze_width / ray[3] * self.cell_width
            length = min(length, self.maze_width)

            if ray[4]:  # If hit a wall
                color = "Blue"  # verticall Wall
                if ray[5]:  # If horizontal Wall
                    color = "Darkblue"
            else:
                color = "Green"
                if ray[5]:
                    color = "Darkgreen"

            pygame.draw.line(
                screen,
                color,
                (current_x, self.maze_width / 2 * 3 - length / 2),
                (current_x, self.maze_width / 2 * 3 + length / 2),
                math.ceil(line_width),
            )

            pygame.draw.line(
                screen,
                "#4f772d",
                (current_x, self.maze_width / 2 * 3 + length / 2),
                (current_x, self.maze_width * 2),
                math.ceil(line_width),
            )

            current_x += line_width

    def ai_view(self, screen: pygame.Surface, maze):
        line_width = self.maze_width / self.rays_amount
        current_x = self.maze_width + line_width / 2
        rays = Raycaster.raycasting(maze, self.rect, self.angle, 90, self.rays_amount)
        for ray in rays:
            length = self.maze_width / ray[3] * self.cell_width
            length = min(length, self.maze_width)

            brightness = max(
                0, min(255, int(255 / (1 + ray[3] * 0.01)))
            )  # Calculate brightness (closer = brighter, farther = darker)

            color = (0, brightness, 0)  # Green with darkness effect
            if ray[4]:  # If hit a wall
                color = (0, 0, brightness)  # Blue with darkness effect

            pygame.draw.line(
                screen,
                color,
                (current_x, self.maze_width / 2 - length / 2),
                (current_x, self.maze_width / 2 + length / 2),
                math.ceil(line_width),
            )

            pygame.draw.line(
                screen,
                "#4f772d",
                (current_x, self.maze_width / 2 + length / 2),
                (current_x, self.maze_width),
                math.ceil(line_width),
            )

            current_x += line_width
