import random


def create_empty_maze(maze_size):
    maze = []
    maze_cell = [1, 1, 0]  # east_wall south_wall visited
    for _ in range(maze_size):
        row = []
        for _ in range(maze_size):
            row.append(maze_cell.copy())
        maze.append(row)
    return maze


def transform_maze(maze):
    maze_size = len(maze)
    new_maze_size = maze_size * 2 - 1
    new_maze = []
    for _ in range(new_maze_size):
        row = [0] * (new_maze_size)
        new_maze.append(row)
    for ir, maze_row in enumerate(maze):
        for ic, maze_cell in enumerate(maze_row):
            if (2 * ic + 1) < new_maze_size and maze_cell[0]:  # east
                new_maze[2 * ir][2 * ic + 1] = 1
            if (2 * ir + 1) < new_maze_size and maze_cell[1]:  # south
                new_maze[2 * ir + 1][2 * ic] = 1
            if (2 * ir + 1) < new_maze_size and (2 * ic + 1) < new_maze_size:
                new_maze[2 * ir + 1][2 * ic + 1] = 1  # corner

    return new_maze


def add_borders(maze):
    maze_size = len(maze)
    new_maze_size = maze_size * 2 + 1
    for maze_row in maze:
        maze_row.insert(0, 1)
        maze_row.append(1)
    maze.insert(0, [1] * new_maze_size)
    maze.append([1] * new_maze_size)
    return maze


def create_maze(maze_size):
    stack = []
    visited_cells = 1
    stack.append([0, 0])
    maze = create_empty_maze(maze_size)
    maze_cells_amount = pow(maze_size, 2)
    maze[0][0][2] = 1
    while visited_cells < maze_cells_amount:
        x, y = stack[len(stack) - 1]
        neighbours = []

        if y > 0 and not maze[y - 1][x][2]:  # North
            neighbours.append(0)

        if y < maze_size - 1 and not maze[y + 1][x][2]:  # South
            neighbours.append(1)

        if x > 0 and not maze[y][x - 1][2]:  # West
            neighbours.append(2)

        if x < maze_size - 1 and not maze[y][x + 1][2]:  # East
            neighbours.append(3)

        if len(neighbours) == 0:
            stack.pop()
            continue

        rand_i = random.randrange(0, len(neighbours))

        match neighbours[rand_i]:
            case 0:  # North
                stack.append([x, y - 1])
                maze[y - 1][x][1] = 0  # South Wall
                maze[y - 1][x][2] = 1
            case 1:  # South
                stack.append([x, y + 1])
                maze[y][x][1] = 0  # South Wall
                maze[y + 1][x][2] = 1
            case 2:  # West
                stack.append([x - 1, y])
                maze[y][x - 1][0] = 0  # East Wall
                maze[y][x - 1][2] = 1
            case 3:  # East
                stack.append([x + 1, y])
                maze[y][x][0] = 0  # East Wall
                maze[y][x + 1][2] = 1

        visited_cells += 1
    maze = transform_maze(maze)
    return add_borders(maze)
