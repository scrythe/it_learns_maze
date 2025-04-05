import neat
import pygame

from game.maze_renderer_with_collision import MazeRendererWithCollision
from game.player import Player


class Game:
    FPS = 60
    MAZE_SIZE = 5

    def __init__(self, max_rounds):
        pygame.init()
        info = pygame.display.Info()
        self.current_size = info.current_h * 0.6
        self.maze = MazeRendererWithCollision(self.MAZE_SIZE)

        self.screen = pygame.display.set_mode(
            (self.current_size, self.current_size), pygame.RESIZABLE
        )
        self.og_screen = pygame.Surface(
            (self.maze.image.get_width() * 2, self.maze.image.get_width() * 2)
        )
        self.clock = pygame.time.Clock()
        self.running = True

        self.players: list[Player] = []
        self.ticks = 0
        self.round = 0
        self.max_rounds = max_rounds

    def setup(self, genomes, config, best_genome):
        if self.round > self.max_rounds:
            self.maze = MazeRendererWithCollision(self.MAZE_SIZE)
            self.round = 0
            if self.max_rounds > 0:
                self.max_rounds -= 0.5
        posx = int(self.maze.cell_width * 1.5)
        best_genome_id = best_genome[0]
        for i, genome in genomes:
            best_genome = False
            if i == best_genome_id:
                best_genome = True
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            player = Player(
                (posx, posx),
                5,
                self.maze.boxes,
                self.maze.boxes_type,
                self.maze.path_cells,
                genome,
                net,
                self.maze.image.get_width(),
                self.maze.cell_width,
                best_genome,
            )
            self.players.append(player)

    def update(self):
        for i, player in enumerate(self.players):
            player.update(self.maze)
            if player.life_time <= 0:
                # print("fitness:", player.genome.fitness)
                del self.players[i]
        self.ticks += 1

    def draw(self):
        self.og_screen.fill("Black")
        self.maze.draw(self.og_screen)
        for player in self.players:
            player.draw(self.og_screen, self.maze)
        pygame.transform.scale(
            self.og_screen,
            (self.screen.get_width(), self.screen.get_height()),
            self.screen,
        )
        pygame.display.update()
