import pygame

import game


class Game:
    TOTAL_WIDTH = 960
    TOTAL_HEIGHT = 720
    FPS = 60

    def __init__(self):
        pygame.init()
        self.maze = game.Maze(5, 50)
        # self.new_maze = game.Maze(5, 50)
        self.screen = pygame.display.set_mode(
            (self.maze.image.width * 2, self.maze.image.height)
        )
        self.clock = pygame.time.Clock()
        self.running = True

        self.players: list[game.Player] = []

        self.setup()

    def setup(self):
        self.maze = game.Maze(5, 50)
        posx = int(self.maze.cell_width * 1.5)
        player = game.Player(
            (posx, posx),
            10,
            self.maze.boxes,
            self.maze.boxes_type,
        )
        self.players.append(player)

    def start(self):
        while self.running:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.update()
            self.draw()

    def update(self):
        if len(self.players) == 0:
            self.setup()
        for i, player in enumerate(self.players):
            player.update(self.maze)
            if player.won:
                del self.players[i]
                return

    def draw(self):
        self.screen.fill("Black")
        self.maze.draw(self.screen)
        for player in self.players:
            player.draw(self.screen)
            player.draw_3D(self.screen, self.maze.image.width, self.maze.cell_width)
        pygame.display.update()
