from game.game import Game
from button import TextButton
import pygame
from game.errors import TerminateWindow
import asyncio

from get_checkpoints import create_checkpoint_id_list, get_checkpoints


async def checkpoint_menu(game: Game):
    running = True
    mouse_checkpoint = 0
    while running:
        checkpoint_menu_title = TextButton(
            game.screen.get_width() / 12,
            "Checkpoint\n   Menu",
            pygame.Color("White"),
            None,
            midtop=(game.screen_rect.centerx, game.screen_rect.centery / 4),
        )

        checkpoints = get_checkpoints()
        checkpoint_id_list = create_checkpoint_id_list(checkpoints, mouse_checkpoint)

        checkpoint_selections: list[TextButton] = []
        for checkpoint_id in checkpoint_id_list:
            if len(checkpoint_selections) < 1:
                bottom_pos = checkpoint_menu_title.image_rect.bottom
            else:
                bottom_pos = checkpoint_selections[-1].image_rect.bottom
            checkpoint_button = TextButton(
                game.screen.get_width() / 20,
                str(checkpoints[checkpoint_id]),
                pygame.Color("#dad7cd"),
                pygame.Color(58, 90, 64, 120),
                midtop=(
                    game.screen_rect.centerx,
                    bottom_pos + game.screen.get_width() / 50,
                ),
            )
            checkpoint_selections.append(checkpoint_button)

        prev_width = game.screen.get_width()
        prev_height = game.screen.get_height()

        mouse_pos = pygame.mouse.get_pos()

        for checkpoint_button in checkpoint_selections:
            checkpoint_button.on_hover(mouse_pos)

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_DOWN:
                    mouse_checkpoint += 1
                    if mouse_checkpoint >= len(checkpoint_id_list):
                        mouse_checkpoint = 0

                if event.key == pygame.K_UP:
                    mouse_checkpoint -= 1
                    if mouse_checkpoint < 0:
                        mouse_checkpoint = len(checkpoint_id_list) - 1

            if event.type == pygame.MOUSEBUTTONDOWN:
                for checkpoint_button in checkpoint_selections:
                    if checkpoint_button.check_click(mouse_pos):
                        return (checkpoint_button.text_input)

        game.screen.fill("#588157")
        checkpoint_menu_title.draw(game.screen)
        for checkpoint_button in checkpoint_selections:
            checkpoint_button.draw(game.screen)

        game.clock.tick(game.FPS)
        pygame.display.update()
        await asyncio.sleep(0)
