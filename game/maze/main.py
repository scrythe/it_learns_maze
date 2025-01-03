import pygame
from game.maze.create_maze import create_maze


class Maze:
    def __init__(self, maze_size: int, cell_width: int) -> None:
        self.maze: list[list[int]] = create_maze(maze_size)
        self.cell_width = cell_width
        maze_surface_size = (len(self.maze)) * cell_width
        self.image = pygame.Surface((maze_surface_size, maze_surface_size))
        self.rect = self.image.get_rect()
        self.walls: list[pygame.Rect] = []
        self.setup(cell_width)

    def setup(self, cell_width: int):
        maze_cell = pygame.Surface((cell_width, cell_width))
        self.image.fill("White")
        current_rect = maze_cell.get_rect()
        for maze_row in self.maze:
            current_rect[0] = 0
            for maze_block in maze_row:
                if maze_block:
                    wall = current_rect.copy()
                    self.image.blit(maze_cell, wall)
                    self.walls.append(wall)
                current_rect.x += cell_width
            current_rect.y += cell_width

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)
