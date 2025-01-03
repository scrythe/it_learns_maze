import pygame
import sys
from os import path


sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from game.maze.create_maze import create_maze
from game.maze.draw_maze import draw_maze

maze_size = 6
cell_width = 50
total_width = (maze_size * 2 + 3) * cell_width
total_height = (maze_size * 2 + 3) * cell_width

pygame.init()
screen = pygame.display.set_mode((total_width, total_height))

maze = create_maze(maze_size)

maze_surface = draw_maze(maze, 50)

maze_pos = maze_surface.get_rect()
maze_pos.center = screen.get_rect().center
screen.blit(maze_surface, maze_pos)

pygame.display.update()
x = input("Hit Enter to Exit")
