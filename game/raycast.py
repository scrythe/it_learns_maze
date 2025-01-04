import math
import game


def raycast_horizontal(maze: game.Maze, player: game.Player):
    ray_x = 0
    ray_y = 0
    off_x = 0
    off_y = 0
    inverse_tan = 1 / math.tan(player.angle)
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
        return None

    maze_size = len(maze.maze)
    depth = maze_size
    while depth:
        mapx: int = int(ray_x / maze.cell_width)
        mapy: int = int((ray_y / maze.cell_width))
        inside_maze = (mapx < maze_size) and (mapx >= 0)
        if not inside_maze:
            return None
        wall = maze.maze[mapy][mapx]
        if wall:
            return (ray_x, ray_y)
        ray_x += off_x
        ray_y += off_y
        depth -= 1
    return (ray_x, ray_y)


def raycast_vertical(maze: game.Maze, player: game.Player):
    ray_x = 0
    ray_y = 0
    off_x = 0
    off_y = 0
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
        return None

    maze_size = len(maze.maze)
    depth = maze_size
    while depth:
        mapx: int = int(ray_x / maze.cell_width)
        mapy: int = int((ray_y / maze.cell_width))
        inside_maze = (mapy < maze_size) and (mapy >= 0)
        if not inside_maze:
            return None
        wall = maze.maze[mapy][mapx]
        if wall:
            return (ray_x, ray_y)
        ray_x += off_x
        ray_y += off_y
        depth -= 1
    return (ray_x, ray_y)


def raycast(maze: game.Maze, player: game.Player):
    # ray = raycast_horizontal(maze, player)
    ray = raycast_vertical(maze, player)
    return ray if ray != None else (0, 0)
