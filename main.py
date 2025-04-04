from typing import Any
import pygame
import neat
import pickle
import argparse

from game.game import Game


def eval_genomes(genomes: list[Any], config, game: Game, render: bool):
    def best_genome_max(genome):  # Used for rendering while training
        if genome[1].fitness == None:
            return -100
        return genome[1].fitness

    best_genome = max(genomes, key=best_genome_max)
    for _, genome in genomes:
        genome.fitness = 0
    game.setup(genomes, config, best_genome)
    while len(game.players):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            # if event.type == pygame.WINDOWRESIZED:
            #     pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            #     game.current_size = 50
            #     game.maze.rescale_image(event.w)
            #     print("hm")
        game.update()
        if render:
            game.draw()
            game.clock.tick(game.FPS)
    game.round += 1


def train_ai(
    config_file: str, game: Game, n_gen: int, render: bool, checkpoint: str | None
):
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file,
    )
    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)
    if checkpoint:
        p = neat.Checkpointer.restore_checkpoint(f"checkpoints/{checkpoint}")

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    checkpointer = neat.Checkpointer(
        generation_interval=5, filename_prefix="checkpoints/neat-checkpoint-"
    )
    p.add_reporter(checkpointer)

    # Damit zusätzliche Parameter mitgegeben werden können
    def execute_eval_genomes_func(genomes, config):
        eval_genomes(genomes, config, game, render)

    # Run for up to "n_gen" amount of generations.
    winner = p.run(execute_eval_genomes_func, n_gen)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)


def test_ai(config_file: str, game: Game):
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file,
    )
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)
    resizing = False
    RESIZE_DELAY = 200
    resize_timer = None
    gen=0
    while game.running or gen > 50:
        game.setup([[0, winner]], config, [0])
        gen+=1
        while len(game.players):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game.running = False
                if event.type == pygame.VIDEORESIZE:
                    resizing = True
                    game.current_size = event.w
                    game.maze.rescale_image(game.current_size)
                # if resizing and event.type != pygame.VIDEORESIZE:
                #     resizing = False
                #     resize_timer = pygame.time.get_ticks()
                # if (
                #     resize_timer != None
                #     and resize_timer + RESIZE_DELAY < pygame.time.get_ticks()
                # ):
                #     resize_timer = None
                #     print(number)
                #     number+=1
                #     pygame.display.set_mode(
                #         (game.current_size, game.current_size), pygame.RESIZABLE
                #     )

            game.update()
            game.draw()
            game.clock.tick(game.FPS)
        game.round += 26


def execute_train_test(
    mode, n_gen=0, render=False, checkpoint: str | None = None, max_rounds=2
):
    if mode == "test":
        game = Game(max_rounds=2)
        test_ai("config.txt", game)
    else:
        game = Game(max_rounds)
        train_ai("config.txt", game, n_gen, render, checkpoint)
    pygame.quit()

def main():
    parser = argparse.ArgumentParser(description="Train or Test a model.")
    parser.add_argument(
        "--mode",
        type=str,
        required=True,
        choices=["train", "test"],
        help="Mode to run the script in: 'train' or 'test'",
    )
    parser.add_argument("--n_gen", type=int, help="Number of generations")
    parser.add_argument(
        "--render",
        type=lambda x: (str(x).lower() == "true"),
        default=False,
        help="Render the game (True/False)",
    )
    parser.add_argument(
        "--checkpoint", type=str, default="", help="Path to checkpoint file (optional)"
    )
    parser.add_argument("--max_rounds", type=int, help="Max rounds per generation")

    args = parser.parse_args()

    execute_train_test(
        args.mode, args.n_gen, args.render, args.checkpoint, args.max_rounds
    )

if __name__ == "__main__":
    main()
