import math
import game


def raycast(maze: game.Maze, player: game.Player):
    ray_x = 0
    ray_y = 0
    off_x = 0
    off_y = 0
    inverse_tan = 1 / math.tan(player.angle)
    if player.angle > math.pi:  # forward
        ray_y = math.floor(player.rect.centery / maze.cell_width) * maze.cell_width
        ray_x = player.rect.centerx - inverse_tan * (player.rect.centery - ray_y)
        off_y = -maze.cell_width
        off_x = off_y * inverse_tan
    elif player.angle < math.pi:  # backward
        ray_y = math.ceil(player.rect.centery / maze.cell_width) * maze.cell_width
        ray_x = player.rect.centerx - inverse_tan * (player.rect.centery - ray_y)
        off_y = maze.cell_width
        off_x = off_y * inverse_tan
    else:  # left or right
        pass
    depth = 8
    while depth:
        # augh
        mapx: int = int(ray_x / maze.cell_width)
        mapy: int = int((ray_y / maze.cell_width)) - 1
        maze_size = len(maze.maze)
        inside_maze = (mapx < maze_size) and (mapx > 0)
        if not inside_maze:
            return (ray_x, ray_y)
        wall = maze.maze[mapy][mapx]
        print(mapy, mapx)
        if wall:
            return (ray_x, ray_y)
        ray_x += off_x
        ray_y += off_y
        depth -= 1
    return (ray_x, ray_y)
