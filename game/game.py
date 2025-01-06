import neat
import pygame

import game


class Game:
    TOTAL_WIDTH = 960
    TOTAL_HEIGHT = 720
    FPS = 60

    def __init__(self):
        pygame.init()
        self.maze = game.Maze(10, 40)
        self.screen = pygame.display.set_mode(
            (self.maze.image.width * 2, self.maze.image.height)
        )
        # self.screen = pygame.display.set_mode(
        #     (self.maze.image.width, self.maze.image.height)
        # )
        self.clock = pygame.time.Clock()
        self.running = True

        self.players: list[game.Player] = []
        self.ticks = 0

    def setup(self, genomes, config):
        self.ticks = 0
        # self.maze = game.Maze(10, 40)
        posx = int(self.maze.cell_width * 1.5)
        best_genome_id = genomes[-1][0]  # id of last genome
        for i, genome in genomes:
            best_genome = False
            if i == best_genome_id:
                best_genome = True
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            player = game.Player(
                (posx, posx),
                5,
                self.maze.boxes,
                self.maze.boxes_type,
                self.maze.path_cells,
                genome,
                net,
                self.maze.image.width,
                self.maze.cell_width,
                best_genome,
            )
            self.players.append(player)

    def update(self):
        if self.ticks > 600:
            for player in self.players:
                player.calculate_fitness()
                # print(player.genome.fitness)
            self.players = []

        for i, player in enumerate(self.players):
            player.update(self.maze)
            if player.won:
                player.calculate_fitness()
                # print(player.genome.fitness)
                del self.players[i]
        self.ticks += 1

    def draw(self):
        self.screen.fill("Black")
        self.maze.draw(self.screen)
        for player in self.players:
            player.draw(self.screen)
            # player.draw_3D(self.screen, self.maze.image.width, self.maze.cell_width)
        pygame.display.update()
