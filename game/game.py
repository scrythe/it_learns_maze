import pygame

class Game:
    TOTAL_WIDTH = 960
    TOTAL_HEIGHT = 720
    FPS = 60

    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((self.TOTAL_WIDTH, self.TOTAL_HEIGHT))
