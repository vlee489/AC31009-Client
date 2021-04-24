import json
from .spriteSheet import SpriteSheet


class CharacterSprite:
    """
    Imports all the sprites for a charecter
    """
    def __init__(self, folder_location: str):
        self.animation_by_id = {}
        self.animations = []
        with open(f"{folder_location}/data.json", "r") as f:
            data = json.load(f)
            for animation in data["sprites"]:
                working_load = SpriteSheet(folder_location, animation['id'])
                self.animations.append(working_load)
                self.animation_by_id[f"{animation['id']}"] = working_load


class AnimationSprite:
    def __init__(self, animation: SpriteSheet, player: int):
        self.animation = animation
        self.player = player
