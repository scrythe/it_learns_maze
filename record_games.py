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

from pygame_screen_record import ScreenRecorder

browser = sys.platform == "emscripten"


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


async def train_ai(game: Game, n_gen: int, render: bool, checkpoint: str):
    p = Checkpointer.restore_checkpoint(f"checkpoints/{checkpoint}")

    async def execute_eval_genomes_func(genomes, config):
        await eval_genomes(genomes, config, game, render)

    await p.run(execute_eval_genomes_func, n_gen)


async def main():
    game = Game(0.5)
    recorder = ScreenRecorder(60, game.og_screen).start_rec()
    game_recordings = 5
    await train_ai(game, game_recordings, True, "neat-checkpoint-1499")
    pygame.quit()
    recorder.stop_rec()  # stop recording
    recorder.save_recording("game_recordings.mp4")  # saves the last recording


if __name__ == "__main__":
    asyncio.run(main())
