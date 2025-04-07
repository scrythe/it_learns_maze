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
from game.errors import TerminateSession, TerminateWindow
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
            pygame.Color("White"),
            None,
            midtop=(game.screen_rect.centerx, game.screen_rect.centery / 4),
        )

        play_button = TextButton(
            game.screen.get_width() / 15,
            "Play",
            pygame.Color("#dad7cd"),
            pygame.Color(58, 90, 64, 120),
            midtop=(
                game.screen_rect.centerx,
                main_menu_title.image_rect.bottom + game.screen.get_width() / 10,
            ),
        )

        test_button = TextButton(
            game.screen.get_width() / 15,
            "Test",
            pygame.Color("#dad7cd"),
            pygame.Color(58, 90, 64, 120),
            midtop=(
                game.screen_rect.centerx,
                play_button.image_rect.bottom + game.screen.get_width() / 15,
            ),
        )

        train_button = TextButton(
            game.screen.get_width() / 15,
            "Train",
            pygame.Color("#dad7cd"),
            pygame.Color(58, 90, 64, 120),
            midtop=(
                game.screen_rect.centerx,
                test_button.image_rect.bottom + game.screen.get_width() / 15,
            ),
        )

        exit_button = TextButton(
            game.screen.get_width() / 15,
            "Exit",
            pygame.Color("#dad7cd"),
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
                    try:
                        await play(game)
                    except TerminateWindow:
                        return
                if test_button.check_click(mouse_pos):
                    try:
                        await test_ai(game)
                    except TerminateWindow:
                        return
                if train_button.check_click(mouse_pos):
                    try:
                        await train_menu(game)
                    except TerminateWindow:
                        return
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


async def train_menu(game: Game):
    running = True
    train_button_selected = False
    train_menu_text = ""
    while running:
        current_train_menu_text = (
            train_menu_text if train_menu_text else "Amount of\nGenerations"
        )

        train_menu_title = TextButton(
            game.screen.get_width() / 12,
            "Train Menu",
            pygame.Color("White"),
            None,
            midtop=(game.screen_rect.centerx, game.screen_rect.centery / 4),
        )

        n_generations_box = TextButton(
            game.screen.get_width() / 20,
            current_train_menu_text,
            pygame.Color("#dad7cd"),
            pygame.Color(58, 90, 64, 120),
            midtop=(
                game.screen_rect.centerx,
                train_menu_title.image_rect.bottom + game.screen.get_width() / 10,
            ),
        )

        train_button = TextButton(
            game.screen.get_width() / 15,
            "Train",
            pygame.Color("#dad7cd"),
            pygame.Color(58, 90, 64, 120),
            midtop=(
                game.screen_rect.centerx,
                n_generations_box.image_rect.bottom + game.screen.get_width() / 15,
            ),
        )

        prev_width = game.screen.get_width()
        prev_height = game.screen.get_height()

        mouse_pos = pygame.mouse.get_pos()

        n_generations_box.on_hover(mouse_pos)
        train_button.on_hover(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise TerminateWindow
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
                if n_generations_box.check_click(mouse_pos):
                    train_button_selected = True
                else:
                    train_button_selected = False
                if train_button.check_click(mouse_pos):
                    if train_menu_text:
                        n_gen = int(train_menu_text)
                    else:
                        n_gen = 500
                    await train_ai(game, n_gen)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if train_button_selected:
                    if event.key == pygame.K_BACKSPACE:
                        train_menu_text = train_menu_text[:-1]
                    else:
                        if event.unicode.isnumeric():
                            train_menu_text += event.unicode

        game.screen.fill("#588157")
        train_menu_title.draw(game.screen)
        n_generations_box.draw(game.screen)
        train_button.draw(game.screen)

        game.clock.tick(game.FPS)
        pygame.display.update()
        await asyncio.sleep(0)


async def train_ai(game: Game, n_gen: int):
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

    game.setup_game(20)
    try:
        # Run for up to "n_gen" amount of generations.
        winner = await p.run(execute_eval_genomes_func, n_gen)
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
