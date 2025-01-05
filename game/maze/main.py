import random
import pygame
from game.maze.create_maze import create_maze


class Maze:
    def __init__(self, maze_size: int, cell_width: int) -> None:
        self.maze: list[list[int]] = create_maze(maze_size)
        self.cell_width = cell_width
        maze_surface_size = (len(self.maze)) * cell_width
        self.image = pygame.Surface((maze_surface_size, maze_surface_size))
        self.rect = self.image.get_rect()
        self.boxes: list[pygame.Rect] = []
        self.boxes_type: list[bool] = []
        self.path_cells: list[pygame.Rect] = []
        self.setup(maze_size, cell_width)

    def setup(self, maze_size: int, cell_width: int):
        # self.create_start_and_end(maze_size)
        self.maze[maze_size * 2 - 1][maze_size * 2 - 1] = 2
        maze_cell = pygame.Surface((cell_width, cell_width))
        goal = maze_cell.copy()
        goal.fill("Blue")
        self.image.fill("White")
        current_rect = maze_cell.get_rect()
        for maze_row in self.maze:
            current_rect[0] = 0
            for maze_block in maze_row:
                if maze_block == 1:
                    wall = current_rect.copy()
                    self.image.blit(maze_cell, wall)
                    self.boxes.append(wall)
                    self.boxes_type.append(False)
                elif maze_block == 2:
                    wall = current_rect.copy()
                    self.image.blit(goal, current_rect)
                    self.boxes.append(wall)
                    self.boxes_type.append(True)
                else:
                    path_cell = current_rect.copy()
                    self.path_cells.append(path_cell)

                current_rect.x += cell_width
            current_rect.y += cell_width

        for i in range(len(self.maze) + 1):
            pygame.draw.line(
                self.image, "Gray", (0, cell_width * i), (self.image.width, cell_width * i), 2
            )  # Vertical Line
            pygame.draw.line(
                self.image, "Gray", (cell_width * i, 0), (cell_width * i, self.image.width), 2
            )  # Horizontal Line

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)

    # def create_start_and_end(self, maze_size: int):
    #     start = random.randrange(maze_size - 1) * 2
    #     if 0 <= start < maze_size:
    #         self.maze[1][start * 2 + 1] = 2  # first free row
    #     elif maze_size <= start < maze_size * 2:
    #         self.maze[(start - maze_size) * 2 + 1][
    #             maze_size * 2 - 1
    #         ] = 2  # last free column
    #     # elif maze_size <= start < maze_size * 2:
    #     #     self.maze[(start - maze_size) * 2 + 1][
    #     #         maze_size * 2 - 1
    #     #     ] = 2  # last free column
