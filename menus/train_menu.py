from typing import Any
from game.game import Game
import pygame
from button import TextButton
from game.errors import TerminateSession, TerminateWindow
import base64
import asyncio
import neat
import pickle
import sys
from menus.checkpoint_menu import checkpoint_menu

browser = True if sys.platform == "emscripten" else False
if browser:
    from platform import window  # type: ignore[attr-defined]


async def train_menu(game: Game):
    current_checkpoint = None
    running = True
    train_button_selected = False
    train_menu_text = ""
    while running:
        current_train_menu_text = (
            train_menu_text if train_menu_text else " Amount of\nGenerations"
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

        checkpoint_text = "Checkpoint:\n"
        amount_spaces = (len(checkpoint_text) - 1) - len(str(current_checkpoint))
        amount_spaces = int(amount_spaces / 2)
        checkpoint_text = (
            checkpoint_text + ' ' * amount_spaces + str(current_checkpoint)
        )
        checkpoint_select_button = TextButton(
            game.screen.get_width() / 20,
            checkpoint_text,
            pygame.Color("#dad7cd"),
            pygame.Color(58, 90, 64, 120),
            midtop=(
                game.screen_rect.centerx,
                n_generations_box.image_rect.bottom + game.screen.get_width() / 15,
            ),
        )

        train_button = TextButton(
            game.screen.get_width() / 15,
            "Train",
            pygame.Color("#dad7cd"),
            pygame.Color(58, 90, 64, 120),
            midtop=(
                game.screen_rect.centerx,
                checkpoint_select_button.image_rect.bottom
                + game.screen.get_width() / 15,
            ),
        )

        prev_width = game.screen.get_width()
        prev_height = game.screen.get_height()

        mouse_pos = pygame.mouse.get_pos()

        n_generations_box.on_hover(mouse_pos)
        checkpoint_select_button.on_hover(mouse_pos)
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
                if checkpoint_select_button.check_click(mouse_pos):
                    await checkpoint_menu(game)
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
        checkpoint_select_button.draw(game.screen)
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
        generation_interval=5, filename_prefix="checkpoints/"
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
