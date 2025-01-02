# class Maze:
#     def __init__(self):
#         maze = []

visited_cells = 0


def create_empty_maze(maze_size):
    maze_cell = [1, 1]  # east south
    maze_row = [maze_cell] * maze_size
    maze_row[maze_size - 1] = [0, 1]
    maze = [maze_row] * (maze_size - 1)
    maze.append([[1, 0]] * maze_size)
    maze[maze_size - 1][maze_size - 1] = [0, 0]
    return maze


def transform_maze(maze):
    maze_size = len(maze)
    new_maze = []
    for _ in range(maze_size * 2 - 1):
        row = [0] * (maze_size * 2 - 1)
        new_maze.append(row)
    for ir, maze_row in enumerate(maze):
        for ic, maze_cell in enumerate(maze_row):
            if maze_cell[0]:  # east
                new_maze[2 * ir][2 * ic + 1] = 1
            if maze_cell[1]:  # south
                new_maze[2 * ir + 1][2 * ic] = 1  # east
    print(new_maze)
    return new_maze


def create_maze(maze_size):
    stack = []
    stack.append([0, 0])
    maze = create_empty_maze(maze_size)
    maze_cells_amount = pow(maze_size, 2)
    while True:
        if visited_cells > maze_cells_amount:
            return maze
