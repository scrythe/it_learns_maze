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

browser = True if sys.platform == "emscripten" else False


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)


async def main():
    game = Game(max_rounds=0.5)

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
                    print("hm")
                if test_button.check_click(mouse_pos):
                    await test_ai(game)
                if train_button.check_click(mouse_pos):
                    pass
                if exit_button.check_click(mouse_pos):
                    running = False

        # await test_ai(game)

        game.screen.fill("#588157")
        main_menu_title.draw(game.screen)
        play_button.draw(game.screen)
        test_button.draw(game.screen)
        train_button.draw(game.screen)
        exit_button.draw(game.screen)

        game.clock.tick(game.FPS)
        pygame.display.update()
        await asyncio.sleep(0)


async def test_ai(game: Game):
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        "config.txt",
    )
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)

    game.running = True
    while game.running:
        game.setup([[0, winner]], config, [0])
        await game.game_loop()


if __name__ == "__main__":
    asyncio.run(main())
