import pygame
from pygame import sprite

from game import player
from game.maze.main import Maze


class Game:
    TOTAL_WIDTH = 960
    TOTAL_HEIGHT = 720
    FPS = 60

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.TOTAL_WIDTH, self.TOTAL_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        self.players = sprite.Group()
        self.maze = Maze(5, 50)

        self.setup()

    def setup(self):
        player.Player((200, 200), 10, self.players, self.maze.walls)

    def start(self):
        while self.running:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.update()
            self.draw()

    def update(self):
        self.players.update()

    def draw(self):
        self.screen.fill("Blue")
        self.maze.draw(self.screen)
        self.players.draw(self.screen)
        pygame.display.update()
