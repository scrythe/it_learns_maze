from typing import Any
import pygame
from game import Game
import os
import neat
import pickle

def eval_genomes(genomes:list[Any], config):
    for _,genome in genomes:
        if genome.fitness== None:
            genome.fitness = 0
    sort_for_best_genome(genomes)
    rounds = 1
    for _,genome in genomes:
        genome.fitness = 0
    for _ in range(rounds):
        game.setup(genomes, config)
        while len(game.players):
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game.running = False
            game.update()
            # game.draw()
            # game.clock.tick(60)

def sort_for_best_genome(genomes):
    def sort_key_func(genome):
        return genome[1].fitness
    genomes.sort(key=sort_key_func)


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
    # p = neat.Checkpointer.restore_checkpoint("neat-checkpoint-999")

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1000))

    # Run for up to 2000 generations.
    winner = p.run(eval_genomes, 2000)
    with open("best.pickle","wb")as f:
        pickle.dump(winner,f)



if __name__ == "__main__":
    game = Game()
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    # import cProfile
    # cProfile.run('run(config_path)')
    run(config_path)
