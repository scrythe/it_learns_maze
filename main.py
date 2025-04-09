# /// script
# dependencies = [
#  "pygame-ce",
# ]
# ///

from typing import Any


import asyncio
import sys
import pygame

from game.game import Game
from button import TextButton
from game.empty_genome import EmptyGenome
from game.errors import TerminateSession, TerminateWindow
from menus.train_menu import train_menu
from menus.test_menu import test_ai


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


if __name__ == "__main__":
    asyncio.run(main())
