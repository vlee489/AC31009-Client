"""
Contains shared functions used between functions
"""
import pygame
from .assets import *


def draw_button(display: pygame.display, rect: pygame.Rect, button_txt: str, disabled=False, small_font=False):
    """
    Draw button
    :param display: display to draw onto
    :param rect: size of button as rect
    :param button_txt: text of button
    :param disabled: if button should be disabled
    :param small_font: to use small font or not
    :return:
    """
    if not disabled:
        outline = black
        fill = light_grey
    else:
        outline = black_transparent
        fill = light_grey_transparent
    if not small_font:
        font = bold_48_font
    else:
        font = regular_29_font
    text_width = font.get_rect(f"{button_txt}")[2]
    text_height = font.get_rect(f"{button_txt}")[3]
    text_x = (rect.x + (rect.width//2)) - (text_width // 2)
    text_y = (rect.y + (rect.height//2)) - (text_height // 2)
    pygame.draw.rect(display, fill, rect)
    pygame.draw.rect(display, outline, rect, 1)
    font.render_to(display, (text_x, text_y), f"{button_txt}", outline)

