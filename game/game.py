import pygame


class Game:
    TOTAL_WIDTH = 960
    TOTAL_HEIGHT = 720
    FPS = 60

    def __init__(self):
        pygame.init()
        pygame.display.set_mode((self.TOTAL_WIDTH, self.TOTAL_HEIGHT))
        self.clock = pygame.time.Clock

    def start(self):
        while True:
            self.update()
            self.draw()
            pygame.time.Clock().tick(5)

    def update(self):
        pass

    def draw(self):
        pygame.display.update()
