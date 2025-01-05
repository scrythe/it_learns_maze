import pygame
from game import Game
import os
import neat

def eval_genomes(genomes, config):
    game.setup(genomes, config)
    while len(game.players):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game.running = False
        game.update()
        game.draw()
        game.clock.tick(60)


def run(config_file: str):
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file,
    )
    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    # Run for up to 300 generations.
    winner = p.run(eval_genomes, 300)


if __name__ == "__main__":
    game = Game()
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    run(config_path)
