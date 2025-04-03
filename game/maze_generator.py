import random

WALL = 1
GOAL = 2

class MazeGenerator:
    @staticmethod
    def generate_maze(size):
        """
        Erstellt ein Irrgarten der angegebenen Größe und gibt es als 2D-Liste zurück.
        """
        grid = MazeGenerator.create_empty_grid(size)
        MazeGenerator.generate_paths(grid, size)
        maze = MazeGenerator.transform_maze(grid, size)
        maze = MazeGenerator.add_borders(maze, size)
        return maze

    @staticmethod
    def create_empty_grid(size):
        """
        Erstellt ein leeres Gitter für das Labyrinth, wobei jede Zelle drei Werte enthält:
        [Ostwand (1 = vorhanden), Südwand (1 = vorhanden), besucht (0 = unbesucht, 1 = besucht)].
        """
        cell_template = [1, 1, 0]  # Standardwerte für jede Zelle
        grid = []
        for _ in range(size):
            row = []
            for _ in range(size):
                row.append(cell_template.copy())
            grid.append(row)
        return grid

    @staticmethod
    def generate_paths(grid, size):
        """
        Erzeugt zufällige Pfade im Labyrinth mit dem Tiefensuchalgorithmus (DFS).
        """
        stack = [(0, 0)]  # Startpunkt (oben links)
        visited_cells = 1
        total_cells = pow(size, 2)
        grid[0][0][2] = 1  # Markiere Startzelle als besucht
        while visited_cells < total_cells:
            x, y = stack[-1]  # Letzte Position im Stack
            neighbors = []

            # Prüfe alle möglichen Nachbarn
            if y > 0 and not grid[y - 1][x][2]:  # Nord
                neighbors.append(0)

            if y < size - 1 and not grid[y + 1][x][2]:  # Süd
                neighbors.append(1)

            if x > 0 and not grid[y][x - 1][2]:  # West
                neighbors.append(2)

            if x < size - 1 and not grid[y][x + 1][2]:  # Ost
                neighbors.append(3)

            if len(neighbors) == 0:
                stack.pop()  # Kein unbesuchter Nachbar -> Zurückgehen
                continue

            rand_i = random.randrange(0, len(neighbors))

            match neighbors[rand_i]:
                case 0:  # Nord
                    stack.append((x, y - 1))
                    grid[y - 1][x][1] = 0  # Entferne Südwand der neuen Zelle
                    grid[y - 1][x][2] = 1  # Markiere als besucht
                case 1:  # Süd
                    stack.append((x, y + 1))
                    grid[y][x][1] = 0  # Entferne Südwand der aktuellen Zelle
                    grid[y + 1][x][2] = 1
                case 2:  # West
                    stack.append((x - 1, y))
                    grid[y][x - 1][0] = 0  # Entferne Ostwand der neuen Zelle
                    grid[y][x - 1][2] = 1
                case 3:  # East
                    stack.append((x + 1, y))
                    grid[y][x][0] = 0  # Entferne Ostwand der aktuellen Zelle
                    grid[y][x + 1][2] = 1

            visited_cells += 1

    @staticmethod
    def transform_maze(grid, size):
        """
        Wandelt das Irrgarten Gitter in eine Matrix um. Eine Zelle ist entweder ein Ziel, eine Wand oder lehr.
        """
        maze_size = size * 2 - 1
        maze = []
        for _ in range(maze_size):
            row = [0] * (maze_size)
            maze.append(row)
        for row_index, row in enumerate(grid):
            for col_index, cell in enumerate(row):
                if (2 * col_index + 1) < maze_size and cell[0]:  # Ostwand
                    maze[2 * row_index][2 * col_index + 1] = WALL
                if (2 * row_index + 1) < maze_size and cell[1]:  # Südwand
                    maze[2 * row_index + 1][2 * col_index] = WALL
                if (2 * row_index + 1) < maze_size and (2 * col_index + 1) < maze_size:
                    maze[2 * row_index + 1][2 * col_index + 1] = WALL  # Eckpunkte

        maze[-1][-1] = GOAL # Setz das Ziel
        return maze

    @staticmethod
    def add_borders(maze, maze_size):
        """
        Fügt eine durchgehende äußere Wand zum Irrgarten hinzu.
        """
        final_size = maze_size * 2 + 1
        for maze_row in maze:
            maze_row.insert(0, 1)  # Links Wand hinzufügen
            maze_row.append(1)  # Rechts Wand hinzufügen
        maze.insert(0, [1] * final_size)  # Oben Wand hinzufügen
        maze.append([1] * final_size)  # Unten Wand hinzufügen
        return maze
