
from game.maze_generator import MazeGenerator, WALL, GOAL
import pygame

class MazeRendererWithCollision:
    def __init__(self, maze_size: int, cell_width: int):
        """
        Initialisiert den Renderer und Kollisionslogik für das Labyrinth.
        """
        self.maze = MazeGenerator.generate_maze(maze_size)
        self.cell_width = cell_width
        maze_surface_size = len(self.maze) * cell_width # Gesamtgröße des Labyrinths in Pixeln
        self.image = pygame.Surface((maze_surface_size, maze_surface_size)) # Erstelle eine Oberfläche für das Labyrinth
        self.rect = self.image.get_rect() # Rechteck für das Labyrinth
        self.boxes: list[pygame.Rect] = []  # Liste zur Speicherung der Rechtecke für Wände und Wege und für Kollision
        self.boxes_type: list[bool] = [] # Liste, die angibt, ob eine Kollision Zelle ein Ziel ist
        self.path_cells: list[pygame.Rect] = [] # Liste der Zellen, die als Pfad markiert sind
        self.setup()

    def setup(self):
        """
        Rendert das Labyrinth auf die Oberfläche und speichert die Positionen der Zellen für Kollisionszwecke.
        """
        maze_cell = pygame.Surface((self.cell_width, self.cell_width))
        maze_cell.fill("Black")
        goal_cell = maze_cell.copy()
        goal_cell.fill("Blue")
        self.image.fill("White")

        current_rect = maze_cell.get_rect()

        for maze_row in self.maze:
            current_rect.x = 0
            for maze_block in maze_row:
                if maze_block == WALL:
                    wall = current_rect.copy()
                    self.image.blit(maze_cell, wall)
                    self.boxes.append(wall)
                    self.boxes_type.append(False)
                elif maze_block == GOAL:
                    wall = current_rect.copy()
                    self.image.blit(goal_cell, current_rect)
                    self.boxes.append(wall)
                    self.boxes_type.append(True)
                else:
                    path_cell = current_rect.copy()
                    self.path_cells.append(path_cell)
                current_rect.x += self.cell_width
            current_rect.y += self.cell_width

        self.draw_grid_lines()

    def draw_grid_lines(self):
        """
        Zeichnet die Gitterlinien für das Labyrinth (die Trennlinien zwischen den Zellen).
        """
        for i in range(len(self.maze) + 1):
            pygame.draw.line(
                self.image,
                "Gray",
                (0, self.cell_width * i),
                (self.image.width, self.cell_width * i),
                2,
            )  # Vertikale Linie
            pygame.draw.line(
                self.image,
                "Gray",
                (self.cell_width * i, 0),
                (self.cell_width * i, self.image.width),
                2,
            )  # Horizontale Linie

    def draw(self, screen: pygame.Surface):
        """
        Zeichnet das Labyrinth auf den angegebenen Bildschirm.
        """
        screen.blit(self.image, self.rect)

