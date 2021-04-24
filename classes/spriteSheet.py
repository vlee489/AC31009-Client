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
                    # Work out how much to scale the sprite by to make it nearly 400 tall
                    self.multiple = 700 // self.sprite_height
                    self.sprite_width = self.sprite_width * self.multiple
                    self.sprite_height = self.sprite_height * self.multiple
                    self.sprite_sheet = pygame.image.load(self.filename)
                    if self.load_mode == "horizontal":
                        y = self.sprite_height
                        x = self.sprite_width * self.frames
                    else:
                        x = self.sprite_width
                        y = self.sprite_height * self.frames
                    # Scale the sprite up
                    self.sprite_sheet = pygame.transform.scale(self.sprite_sheet, (x, y))
                    return
            raise Exception("no sprite with ID")

    @property
    def animation_played_through(self) -> bool:
        if self.next_frame == 1:
            return True
        else:
            return False

    @property
    def get_next_frame(self):
        # work out where to cut sprite out from
        if self.load_mode == "horizontal":
            y = 0
            x = (self.next_frame - 1) * self.sprite_width
        elif self.load_mode == "vertical":
            x = 0
            y = (self.next_frame - 1) * self.sprite_height
        else:
            raise Exception("Invalid load mode")
        # work out next frame and store
        self.next_frame += 1
        if self.next_frame > self.frames:
            self.next_frame = 1
        return self.sprite_sheet.subsurface(pygame.Rect(x, y, self.sprite_width, self.sprite_height))