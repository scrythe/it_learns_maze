# class Maze:
#     def __init__(self):
#         maze = []


def create_empty_maze_row(width):
    row = []
    for _ in range(width - 1):
        row.append(0)
        row.append(1)
    row.append(0)
    return row


def create_empty_maze(width):
    maze = []
    empty_maze_row = create_empty_maze_row(width)
    for _ in range(width - 1):
        maze.append(empty_maze_row)
        maze.append([1] * (2 * width - 1))
    maze.append(empty_maze_row)
    return maze
