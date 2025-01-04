import math

import pygame
import game


def raycast_horizontal(
    maze, cell_width: int, rect: pygame.FRect, angle: float
) -> tuple[float, float, float]:
    ray_x = 0
    ray_y = 0
    off_x = 0
    off_y = 0

    maze_size = len(maze)
    maze_width = maze_size * cell_width

    if angle == 0:
        return (0, 0, maze_width)
    inverse_tan = 1 / math.tan(angle)


    if angle > math.pi:  # forward
        ray_y = math.floor(rect.centery / cell_width) * cell_width - 0.0001
        ray_sin = rect.centery - ray_y
        ray_cos = inverse_tan * ray_sin
        ray_x = rect.centerx - ray_cos
        off_y = -cell_width
        off_x = off_y * inverse_tan
    elif angle < math.pi:  # backward
        ray_y = math.ceil(rect.centery / cell_width) * cell_width
        ray_sin = rect.centery - ray_y
        ray_cos = inverse_tan * ray_sin
        ray_x = rect.centerx - ray_cos
        off_y = cell_width
        off_x = off_y * inverse_tan
    else:  # left or right
        return (0, 0, maze_width)

    depth = maze_size
    while depth:
        mapx: int = int(ray_x / cell_width)
        mapy: int = int((ray_y / cell_width))
        inside_maze = (mapx < maze_size) and (mapx >= 0)
        if not inside_maze:
            return (0, 0, maze_width)
        wall = maze[mapy][mapx]
        if wall:
            ray_len_x = rect.centerx - ray_x
            ray_len_y = rect.centery - ray_y
            ray_len = math.sqrt(math.pow(ray_len_x, 2) + math.pow(ray_len_y, 2))
            return (ray_x, ray_y, ray_len)
        ray_x += off_x
        ray_y += off_y
        depth -= 1
    return (0, 0, maze_width)


def raycast_vertical(
    maze, cell_width: int, rect: pygame.FRect, angle: float
) -> tuple[float, float, float]:
    ray_x = 0
    ray_y = 0
    off_x = 0
    off_y = 0

    maze_size = len(maze)
    maze_width = maze_size * cell_width

    if (angle > math.pi / 2) and (angle < 3 * math.pi / 2):  # left
        ray_x = math.floor(rect.centerx / cell_width) * cell_width - 0.0001
        ray_cos = rect.centerx - ray_x
        ray_sin = math.tan(angle) * ray_cos
        ray_y = rect.centery - ray_sin
        off_x = -cell_width
        off_y = off_x * math.tan(angle)
    elif (angle < math.pi / 2) or (angle > 3 * math.pi / 2):
        ray_x = math.ceil(rect.centerx / cell_width) * cell_width
        ray_cos = rect.centerx - ray_x
        ray_sin = math.tan(angle) * ray_cos
        ray_y = rect.centery - ray_sin
        off_x = cell_width
        off_y = off_x * math.tan(angle)
    else:  # forward or backwards
        return (0, 0, maze_width)

    depth = maze_size
    while depth:
        mapx: int = int(ray_x / cell_width)
        mapy: int = int((ray_y / cell_width))
        inside_maze = (mapy < maze_size) and (mapy >= 0)
        if not inside_maze:
            return (0, 0, maze_width)
        wall = maze[mapy][mapx]
        if wall:
            ray_len_x = rect.centerx - ray_x
            ray_len_y = rect.centery - ray_y
            ray_len = math.sqrt(math.pow(ray_len_x, 2) + math.pow(ray_len_y, 2))
            return (ray_x, ray_y, ray_len)

        ray_x += off_x
        ray_y += off_y
        depth -= 1
    return (0, 0, maze_width)


def raycast(maze: game.Maze, player: game.Player, angle: float):
    ray_h = raycast_horizontal(maze.maze, maze.cell_width, player.rect, angle)
    ray_v = raycast_vertical(maze.maze, maze.cell_width, player.rect, angle)
    ray = min(ray_h, ray_v, key=lambda ray: ray[2])
    return (ray[0], ray[1])


def raycasting(maze: game.Maze, player: game.Player, fov, amount):
    fov_rad = math.radians(fov)
    fov_step = fov_rad / amount
    rays: list[tuple[float, float]] = []
    for current_step in range(amount):
        angle = player.angle - fov_rad / 2 + fov_step * current_step
        if angle < 0:
            angle += 2 * math.pi
        if angle > 2 * math.pi:
            angle -= 2 * math.pi
        rays.append(raycast(maze, player, angle))
    return rays
