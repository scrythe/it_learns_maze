from typing import Any
import pygame
from game import Game
import os
import neat
import pickle


def eval_genomes(genomes: list[Any], config):
    def best_genome_max(genome):
        if genome[1].fitness == None:
            return -100
        return genome[1].fitness
    best_genome = max(genomes, key=best_genome_max)

    print(best_genome)
    for _, genome in genomes:
        genome.fitness = 0
    game.setup(genomes, config, best_genome)
    while len(game.players):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
        game.update()
        game.draw()
        # input("")
        game.clock.tick(60)
    game.round += 1


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
    # p = neat.Checkpointer.restore_checkpoint("neat-checkpoint-10269")

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    # Run for up to 2000 generations.
    winner = p.run(eval_genomes, 20000)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)


if __name__ == "__main__":
    game = Game()
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    # import cProfile
    # cProfile.run('run(config_path)')
    run(config_path)
