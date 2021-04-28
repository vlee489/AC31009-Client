"""
Holds random assets that are used such as colours
"""
from pygame import Color, Rect, freetype
from .characterSprite import CharacterSprite

# Colours
light_grey = Color('#E9E9E9')
light_grey_transparent = Color(233, 233, 233, 50)
black_transparent = (0, 0, 0, 50)
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
green = Color('#0EA453')
blue = Color('#49B4F0')

# Font
freetype.init()
bold_64_font = freetype.Font("assets/Montserrat/Montserrat-Bold.ttf", 64)
bold_48_font = freetype.Font("assets/Montserrat/Montserrat-Bold.ttf", 48)
bold_36_font = freetype.Font("assets/Montserrat/Montserrat-Bold.ttf", 36)
regular_48_font = freetype.Font("assets/Montserrat/Montserrat-Regular.ttf", 48)
regular_29_font = freetype.Font("assets/Montserrat/Montserrat-Regular.ttf", 29)
regular_18_font = freetype.Font("assets/Montserrat/Montserrat-Regular.ttf", 18)

# Icons
back_icon = transform.scale(image.load("assets/icons/back.png"), (85, 85))

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
# Move Type Select
attack_move_rect = Rect(182, 890, 350, 120)
item_move_rect = Rect(586, 890, 350, 120)
shield_rect = Rect(990, 890, 350, 120)
skip_rect = Rect(1394, 890, 350, 120)

back_button_rect = Rect(101, 890, 120, 120)

# This is used to tell the game what sprite to use for each HeroID by folder name of sprite
sprite_data = {
    1: CharacterSprite("assets/Sprites/HeroKnight"),
    2: CharacterSprite("assets/Sprites/WizardPack"),
    3: CharacterSprite("assets/Sprites/SpiritBoxer"),
}
