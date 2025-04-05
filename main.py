# /// script
# dependencies = [
#  "pygame-ce",
# ]
# ///

from typing import Any
import pygame
from neat import (
    DefaultGenome,
    DefaultReproduction,
    DefaultSpeciesSet,
    DefaultStagnation,
    Population,
    Config,
    Checkpointer,
    StdOutReporter,
    StatisticsReporter,
)
import pickle
import argparse
import asyncio
import sys

from game.game import Game

browser = True if sys.platform == "emscripten" else False


async def eval_genomes(genomes: list[Any], config, game: Game, render: bool):
    def best_genome_max(genome):  # Used for rendering while training
        if genome[1].fitness == None:
            return -100
        return genome[1].fitness

    best_genome = max(genomes, key=best_genome_max)
    for _, genome in genomes:
        genome.fitness = 0
    game.setup(genomes, config, best_genome)
    while game.running and len(game.players):
        prev_width = game.screen.get_width()
        prev_height = game.screen.get_height()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
                pygame.quit()
                sys.exit()

            if not browser:
                if event.type == pygame.VIDEORESIZE:
                    if abs(prev_width - event.w) > abs(prev_height - event.h):
                        prev_width = event.w
                        prev_height = event.h
                        game.screen = pygame.display.set_mode(
                            (event.w, event.w), pygame.RESIZABLE
                        )
                    else:
                        prev_width = event.w
                        prev_height = event.h
                        game.screen = pygame.display.set_mode(
                            (event.h, event.h), pygame.RESIZABLE
                        )

        game.update()
        if render:
            game.draw()
            game.clock.tick(game.FPS)
            await asyncio.sleep(0)
    game.round += 1


async def train_ai(
    config_file: str, game: Game, n_gen: int, render: bool, checkpoint: str | None
):
    config = Config(
        DefaultGenome,
        DefaultReproduction,
        DefaultSpeciesSet,
        DefaultStagnation,
        config_file,
    )
    # Create the population, which is the top-level object for a NEAT run.
    p = Population(config)
    if checkpoint:
        p = Checkpointer.restore_checkpoint(f"checkpoints/{checkpoint}")

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(StdOutReporter(True))
    stats = StatisticsReporter()
    p.add_reporter(stats)
    checkpointer = Checkpointer(
        generation_interval=5, filename_prefix="checkpoints/neat-checkpoint-"
    )
    p.add_reporter(checkpointer)

    # Damit zusätzliche Parameter mitgegeben werden können
    async def execute_eval_genomes_func(genomes, config):
        await eval_genomes(genomes, config, game, render)

    # Run for up to "n_gen" amount of generations.
    winner = await p.run(execute_eval_genomes_func, n_gen)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)


async def test_ai(config_file: str, game: Game):
    config = Config(
        DefaultGenome,
        DefaultReproduction,
        DefaultSpeciesSet,
        DefaultStagnation,
        config_file,
    )
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)
    while game.running:
        game.setup([[0, winner]], config, [0])
        while game.running and len(game.players):
            prev_width = game.screen.get_width()
            prev_height = game.screen.get_height()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game.running = False

                if not browser:
                    if event.type == pygame.VIDEORESIZE:
                        if abs(prev_width - event.w) > abs(prev_height - event.h):
                            prev_width = event.w
                            prev_height = event.h
                            game.screen = pygame.display.set_mode(
                                (event.w, event.w), pygame.RESIZABLE
                            )
                        else:
                            prev_width = event.w
                            prev_height = event.h
                            game.screen = pygame.display.set_mode(
                                (event.h, event.h), pygame.RESIZABLE
                            )

            game.update()
            game.draw()
            game.clock.tick(game.FPS)
            await asyncio.sleep(0)
        game.round += 1


async def execute_train_test(
    mode, n_gen=0, render=False, checkpoint: str | None = None, max_rounds=2
):
    if mode == "test":
        game = Game(max_rounds=2)
        await test_ai("config.txt", game)
    else:
        game = Game(max_rounds)
        await train_ai("config.txt", game, n_gen, render, checkpoint)
    pygame.quit()


async def main():
    parser = argparse.ArgumentParser(description="Train or Test a model.")
    # parser.add_argument(
    #     "--mode",
    #     type=str,
    #     required=True,
    #     choices=["train", "test"],
    #     help="Mode to run the script in: 'train' or 'test'",
    # )
    # parser.add_argument("--n_gen", type=int, help="Number of generations")
    # parser.add_argument(
    #     "--render",
    #     type=lambda x: (str(x).lower() == "true"),
    #     default=False,
    #     help="Render the game (True/False)",
    # )
    # parser.add_argument(
    #     "--checkpoint", type=str, default="", help="Path to checkpoint file (optional)"
    # )
    # parser.add_argument("--max_rounds", type=int, help="Max rounds per generation")

    # args = parser.parse_args()
    # print("args:" + args)

    # execute_train_test(
    #     args.mode, args.n_gen, args.render, args.checkpoint, args.max_rounds
    # )

    await execute_train_test("train", 500, True, "neat-checkpoint-1499", 2)
    # await execute_train_test("test")


if __name__ == "__main__":
    asyncio.run(main())
