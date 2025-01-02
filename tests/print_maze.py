import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from game.maze import create_empty_maze, transform_maze

maze = create_empty_maze(4)
print(maze)
print(transform_maze(maze))
