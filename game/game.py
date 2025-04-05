import neat
import pygame

from game.maze_renderer_with_collision import MazeRendererWithCollision
from game.player import Player
import sys


class Game:
    FPS = 60
    MAZE_SIZE = 5

    def __init__(self, max_rounds):
        pygame.init()
        info = pygame.display.Info()
        current_size = info.current_h * 0.9
        self.maze = MazeRendererWithCollision(self.MAZE_SIZE)
        self.browser = True if sys.platform == "emscripten" else False

        if self.browser:
            self.screen = pygame.display.set_mode(
                (self.maze.image.get_width() * 2, self.maze.image.get_width() * 2)
            )
        else:
            self.screen = pygame.display.set_mode(
                (current_size, current_size), pygame.RESIZABLE
            )
            self.og_screen = pygame.Surface(
                (self.maze.image.get_width() * 2, self.maze.image.get_width() * 2)
            )
        self.clock = pygame.time.Clock()
        self.running = True

        self.players: list[Player] = []
        self.dead_players: list[Player] = []
        self.ticks = 0
        self.round = 0
        self.max_rounds = max_rounds

    def setup(self, genomes, config, best_genome):
        self.dead_players = []
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
            if best_genome:
                self.best_player = player
            self.players.append(player)

    def update(self):
        for i, player in enumerate(self.players):
            player.update(self.maze)
            if player.life_time <= 0:
                self.dead_players.append(self.players[i])
                del self.players[i]
        self.ticks += 1

    def normal_draw(self, screen: pygame.Surface):
        screen.fill("Black")
        self.maze.draw(screen)
        for player in self.dead_players:
            player.normal_draw(screen)
        for player in self.players:
            player.normal_draw(screen)
        # Seperate to draw on top of other players
        self.best_player.best_player_draw(screen, self.maze)

    def draw(self):
        if self.browser:
            self.normal_draw(self.screen)
        else:
            self.normal_draw(self.og_screen)
            pygame.transform.scale(
                self.og_screen,
                (self.screen.get_width(), self.screen.get_height()),
                self.screen,
            )
        pygame.display.update()
