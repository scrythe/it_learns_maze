# /// script
# dependencies = [
#  "pygame-ce",
# ]
# ///

from typing import Any


import asyncio
import sys
import pygame
import neat
import pickle

from game.game import Game
from button import TextButton
from game.empty_genome import EmptyGenome
from game.terminate_session import TerminateSession
import base64


browser = True if sys.platform == "emscripten" else False

if browser:
    from platform import window  # type: ignore[attr-defined]


async def main():
    game = Game(browser)

    running = True
    while running:
        main_menu_title = TextButton(
            game.screen.get_width() / 12,
            "Main Menu",
            "White",
            None,
            midtop=(game.screen_rect.centerx, game.screen_rect.centery / 4),
        )

        play_button = TextButton(
            game.screen.get_width() / 15,
            "Play",
            "#dad7cd",
            pygame.Color(58, 90, 64, 120),
            midtop=(
                game.screen_rect.centerx,
                main_menu_title.image_rect.bottom + game.screen.get_width() / 10,
            ),
        )

        test_button = TextButton(
            game.screen.get_width() / 15,
            "Test",
            "#dad7cd",
            pygame.Color(58, 90, 64, 120),
            midtop=(
                game.screen_rect.centerx,
                play_button.image_rect.bottom + game.screen.get_width() / 15,
            ),
        )

        train_button = TextButton(
            game.screen.get_width() / 15,
            "Train",
            "#dad7cd",
            pygame.Color(58, 90, 64, 120),
            midtop=(
                game.screen_rect.centerx,
                test_button.image_rect.bottom + game.screen.get_width() / 15,
            ),
        )

        exit_button = TextButton(
            game.screen.get_width() / 15,
            "Exit",
            "#dad7cd",
            pygame.Color(58, 90, 64, 120),
            midtop=(
                game.screen_rect.centerx,
                train_button.image_rect.bottom + game.screen.get_width() / 15,
            ),
        )

        prev_width = game.screen.get_width()
        prev_height = game.screen.get_height()

        mouse_pos = pygame.mouse.get_pos()

        play_button.on_hover(mouse_pos)
        test_button.on_hover(mouse_pos)
        train_button.on_hover(mouse_pos)
        exit_button.on_hover(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                if abs(prev_width - event.w) > abs(prev_height - event.h):
                    prev_width = event.w
                    prev_height = event.h
                    game.screen = pygame.display.set_mode(
                        (event.w, event.w), pygame.RESIZABLE
                    )
                    game.screen_rect = game.screen.get_rect()
                else:
                    prev_width = event.w
                    prev_height = event.h
                    game.screen = pygame.display.set_mode(
                        (event.h, event.h), pygame.RESIZABLE
                    )
                    game.screen_rect = game.screen.get_rect()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.check_click(mouse_pos):
                    await play(game)
                if test_button.check_click(mouse_pos):
                    await test_ai(game)
                if train_button.check_click(mouse_pos):
                    await train_ai(game)
                if not browser:
                    if exit_button.check_click(mouse_pos):
                        running = False

        # await test_ai(game)

        game.screen.fill("#588157")
        main_menu_title.draw(game.screen)
        play_button.draw(game.screen)
        test_button.draw(game.screen)
        train_button.draw(game.screen)
        if not browser:
            exit_button.draw(game.screen)

        game.clock.tick(game.FPS)
        pygame.display.update()
        await asyncio.sleep(0)


async def play(game: Game):
    game.setup_game(0.5)
    while True:
        empty_genome = EmptyGenome()
        game.setup_ai_env(
            genomes=[[0, empty_genome]], config=None, best_genome=[0], ai=False
        )
        try:
            await game.game_loop()
        except TerminateSession:
            return
        game.round += 1


async def test_ai(game: Game):
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        "config.txt",
    )

    if browser:
        pickled_data_b64 = window.localStorage.getItem("best.pickle")
        if not pickled_data_b64:
            return
        pickle_data = base64.b64decode(pickled_data_b64)
        winner = pickle.loads(pickle_data)
    else:
        with open("best.pickle", "rb") as f:
            winner = pickle.load(f)

    game.setup_game(0.5)
    while True:
        game.setup_ai_env(
            genomes=[[0, winner]], config=config, best_genome=[0], ai=True
        )
        try:
            await game.game_loop()
        except TerminateSession:
            return
        game.round += 1


async def train_ai(game: Game):
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        "config.txt",
    )
    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)
    # if checkpoint:
    #     p = neat.Checkpointer.restore_checkpoint(f"checkpoints/{checkpoint}")

    checkpointer = neat.Checkpointer(
        generation_interval=5, filename_prefix="checkpoints/neat-checkpoint-"
    )
    p.add_reporter(checkpointer)

    # Damit zusätzliche Parameter mitgegeben werden können
    async def execute_eval_genomes_func(genomes, config):
        await eval_genomes(genomes, config, game)

    # Run for up to "n_gen" amount of generations.
    game.setup_game(20)
    try:
        winner = await p.run(execute_eval_genomes_func, 50)
    except TerminateSession:
        winner = p.best_genome

    if winner:
        if browser:
            pickled_data = pickle.dumps(winner)
            pickled_data_b64 = base64.b64encode(pickled_data).decode("utf-8")
            window.localStorage.setItem("best.pickle", pickled_data_b64)
        else:
            with open("best.pickle", "wb") as f:
                pickle.dump(winner, f)


async def eval_genomes(genomes: list[Any], config, game: Game):
    def best_genome_max(genome):
        if genome[1].fitness == None:
            return -100
        return genome[1].fitness

    best_genome = max(genomes, key=best_genome_max)
    for _, genome in genomes:
        genome.fitness = 0
    game.setup_ai_env(genomes, config, best_genome, ai=True)
    await game.game_loop()
    game.round += 1


if __name__ == "__main__":
    asyncio.run(main())
