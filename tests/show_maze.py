import pygame
import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from game import create_empty_maze

maze_width = 10
cell_width = 50
total_width = (maze_width * 2 + 1) * cell_width
total_height = (maze_width * 2 + 1) * cell_width

pygame.init()
screen = pygame.display.set_mode((total_width, total_height))

# maze = [
#     [0, 0, 0, 0],
#     [1, 1, 0, 0],
#     [0, 0, 1, 0],
#     [0, 0, 0, 1],
# ]

maze = create_empty_maze(10)


def draw_maze():
    screen.get_rect().center
    cell = pygame.Surface((cell_width, cell_width))
    current_pos = [cell_width, cell_width]
    wall = cell.__copy__()
    cell.fill("Red")
    wall.fill("blue")
    for maze_row in maze:
        current_pos[0] = cell_width
        for maze_block in maze_row:
            if maze_block:
                screen.blit(cell, current_pos)
            else:
                screen.blit(wall, current_pos)
            current_pos[0] += cell_width
        current_pos[1] += cell_width


draw_maze()

pygame.display.update()
x = input("Hit Enter to Exit")
