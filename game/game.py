import pygame
from pygame import sprite

from game import player


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
        self.walls = sprite.Group()

        self.setup()

    def setup(self):
        player.Player((200, 200), 20, self.players, self.walls)

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
        self.players.draw(self.screen)
        pygame.display.update()
