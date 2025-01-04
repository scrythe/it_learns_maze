import math
import game


def raycast_horizontal(maze: game.Maze, player: game.Player):
    ray_x = 0
    ray_y = 0
    off_x = 0
    off_y = 0
    inverse_tan = 1 / math.tan(player.angle)

    maze_size = len(maze.maze)
    maze_width = maze_size * maze.cell_width

    if player.angle > math.pi:  # forward
        ray_y = (
            math.floor(player.rect.centery / maze.cell_width) * maze.cell_width - 0.0001
        )
        ray_sin = player.rect.centery - ray_y
        ray_cos = inverse_tan * ray_sin
        ray_x = player.rect.centerx - ray_cos
        off_y = -maze.cell_width
        off_x = off_y * inverse_tan
    elif player.angle < math.pi:  # backward
        ray_y = math.ceil(player.rect.centery / maze.cell_width) * maze.cell_width
        ray_sin = player.rect.centery - ray_y
        ray_cos = inverse_tan * ray_sin
        ray_x = player.rect.centerx - ray_cos
        off_y = maze.cell_width
        off_x = off_y * inverse_tan
    else:  # left or right
        return (0, 0, maze_width)

    depth = maze_size
    while depth:
        mapx: int = int(ray_x / maze.cell_width)
        mapy: int = int((ray_y / maze.cell_width))
        inside_maze = (mapx < maze_size) and (mapx >= 0)
        if not inside_maze:
            return (0, 0, maze_width)
        wall = maze.maze[mapy][mapx]
        if wall:
            ray_len_x = player.rect.centerx - ray_x
            ray_len_y = player.rect.centery - ray_y
            ray_len = math.sqrt(math.pow(ray_len_x, 2) + math.pow(ray_len_y, 2))
            return (ray_x, ray_y, ray_len)
        ray_x += off_x
        ray_y += off_y
        depth -= 1
    return (0, 0, maze_width)


def raycast_vertical(maze: game.Maze, player: game.Player):
    ray_x = 0
    ray_y = 0
    off_x = 0
    off_y = 0

    maze_size = len(maze.maze)
    maze_width = maze_size * maze.cell_width

    if (player.angle > math.pi / 2) and (player.angle < 3 * math.pi / 2):  # left
        ray_x = (
            math.floor(player.rect.centerx / maze.cell_width) * maze.cell_width - 0.0001
        )
        ray_cos = player.rect.centerx - ray_x
        ray_sin = math.tan(player.angle) * ray_cos
        ray_y = player.rect.centery - ray_sin
        off_x = -maze.cell_width
        off_y = off_x * math.tan(player.angle)
    elif (player.angle < math.pi / 2) or (player.angle > 3 * math.pi / 2):
        ray_x = math.ceil(player.rect.centerx / maze.cell_width) * maze.cell_width
        ray_cos = player.rect.centerx - ray_x
        ray_sin = math.tan(player.angle) * ray_cos
        ray_y = player.rect.centery - ray_sin
        off_x = maze.cell_width
        off_y = off_x * math.tan(player.angle)
    else:  # forward or backwards
        return (0, 0, maze_width)

    depth = maze_size
    while depth:
        mapx: int = int(ray_x / maze.cell_width)
        mapy: int = int((ray_y / maze.cell_width))
        inside_maze = (mapy < maze_size) and (mapy >= 0)
        if not inside_maze:
            return (0, 0, maze_width)
        wall = maze.maze[mapy][mapx]
        if wall:
            ray_len_x = player.rect.centerx - ray_x
            print(player.rect.centerx, ray_x)
            ray_len_y = player.rect.centery - ray_y
            ray_len = math.sqrt(math.pow(ray_len_x, 2) + math.pow(ray_len_y, 2))
            return (ray_x, ray_y, ray_len)

        ray_x += off_x
        ray_y += off_y
        depth -= 1
    return (0, 0, maze_width)


def raycast(maze: game.Maze, player: game.Player):
    ray_h = raycast_horizontal(maze, player)
    ray_v = raycast_vertical(maze, player)
    ray = min(ray_h, ray_v, key=lambda ray: ray[2])
    print(ray_h[2], ray_v[2], ray[2])
    return ray
