import pygame

from game import Game


def main():
    Game()
    while True:
        pygame.display.update()


if __name__ == "__main__":
    main()
    pygame.init()
