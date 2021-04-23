import pygame
import json


class SpriteSheet:
    def __init__(self, root_location: str, sprite_id: int):
        self.next_frame = 1
        with open(f"{root_location}\\data.json", "r") as file:
            data = json.load(file)
            for option in data["sprites"]:
                if option["id"] == sprite_id:
                    self.name = option["name"]
                    self.filename = f"{root_location}\\{option['file']}"
                    self.sprite_height = option['spriteHeight']
                    self.sprite_width = option['spriteWidth']
                    self.frames = option['frames']
                    self.load_mode = option['load']
                    self.sprite_sheet = pygame.image.load(self.filename).convert()
            raise Exception("no sprite with ID")

    @property
    def animation_played_through(self) -> bool:
        if self.next_frame == 1:
            return True
        else:
            return False

    def get_next_frame(self):
        # setup sprite surface
        sprite = pygame.Surface((self.sprite_width, self.sprite_height))
        sprite.set_colorkey((0, 0, 0))
        # work out where to cut sprite out from
        if self.load_mode == "horizontal":
            y = self.sprite_height
            x = (self.next_frame - 0) * self.sprite_width
        elif self.load_mode == "vertical":
            x = self.sprite_width
            y = (self.next_frame - 0) * self.sprite_height
        else:
            x = 100
            y = 100
        rect = pygame.Rect(x, y, self.sprite_width, self.sprite_height)
        sprite.blit(self.sprite_sheet, (0, 0), rect)
        # work out next frame and store
        self.next_frame += 1
        if self.next_frame > self.frames:
            self.next_frame = 0
        return sprite
