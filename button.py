import pygame
from typing import Any


class TextButton:
    def __init__(
        self,
        size: float,
        text_input: str,
        text_color: pygame.color.Color,
        background_color: pygame.color.Color,
        **position: Any,
    ):
        self.text_input = text_input
        self.font = pygame.font.Font(
            "assets/Press_Start_2P/PressStart2P-Regular.ttf", int(size)
        )
        self.text = self.font.render(self.text_input, True, text_color)
        self.text_rect = self.text.get_rect(**position)

        padding = self.text_rect.height * 0.5
        self.image = pygame.Surface(
            (self.text_rect.width + padding, self.text_rect.height + padding),
            pygame.SRCALPHA,
        )
        self.image_rect = self.image.get_rect(center=self.text_rect.center)

        # self.image.set_colorkey((0, 0, 0))

        if background_color:
            self.image.fill(background_color)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.image_rect)
        screen.blit(self.text, self.text_rect)

    def on_hover(self, mouse_pos: tuple[int, int]):
        if mouse_pos[0] in range(
            self.image_rect.left, self.image_rect.right
        ) and mouse_pos[1] in range(self.image_rect.top, self.image_rect.bottom):
            self.text = self.font.render(self.text_input, True, "White")

    def check_click(self, mouse_pos: tuple[int, int]):
        if mouse_pos[0] in range(
            self.image_rect.left, self.image_rect.right
        ) and mouse_pos[1] in range(self.image_rect.top, self.image_rect.bottom):
            return True
        return False
