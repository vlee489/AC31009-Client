"""
Holds random assets that are used such as colours
"""
from pygame import Color, Rect
import pygame.freetype

# Colours
light_grey = Color('#E9E9E9')
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

# Font
pygame.freetype.init()
bold_48_font = pygame.freetype.Font("assets/Montserrat/Montserrat-Bold.ttf", 48)
bold_36_font = pygame.freetype.Font("assets/Montserrat/Montserrat-Bold.ttf", 36)
regular_29_font = pygame.freetype.Font("assets/Montserrat/Montserrat-Regular.ttf", 29)
regular_18_font = pygame.freetype.Font("assets/Montserrat/Montserrat-Regular.ttf", 18)

# Rects
# ==============
return_to_rect = Rect(48, 944, 330, 100)
# Menu
join_lobby_rect = Rect(695, 210, 530, 120)
create_lobby_rect = Rect(695, 405, 530, 120)
view_stats_rect = Rect(695, 600, 530, 120)
exit_main_menu_rect = Rect(695, 795, 530, 120)
# Hero Select
hero_1_rect = Rect(188, 877, 350, 120)
hero_2_rect = Rect(592, 877, 350, 120)
hero_3_rect = Rect(996, 877, 350, 120)
hero_4_rect = Rect(1387, 877, 350, 120)
# Lobby Code Enter
enter_lobby_rect = Rect(682, 584, 530, 120)
