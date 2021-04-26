from .gameData import HeroData
from .characterSprite import CharacterSprite


class PlayerStats:
    """
    Stores data of players character and their current stats
    """

    def __init__(self, HP: int, shield: int, speed: int, speed_length: int):
        self.HP = HP
        self.shield = shield
        self.speed = speed
        self.speed_length = speed_length
        self.previous_hp = HP
        self.previous_shield = shield

    def set_stats(self, HP: int, shield: int, speed: int, speed_length: int):
        """
        Sets stats
        :param HP: hp
        :param shield: shield
        :param speed: speed
        :param speed_length: speed_length
        :return:
        """
        self.HP = HP
        self.shield = shield
        self.speed = speed
        self.speed_length = speed_length

    @property
    def get_hp_diff(self):
        diff = self.previous_hp - self.HP
        self.previous_hp = self.HP
        return diff

    @property
    def get_shield_diff(self):
        diff = self.previous_shield - self.shield
        self.previous_shield = self.shield
        return diff


class Player:
    """
    Stores data on a player
    """
    hero: HeroData

    def __init__(self, username: str, user_id: str, hero: HeroData,  hp: int, shield: int,
                 speed: int, speed_length: int, char_sprite: CharacterSprite):
        self.username = username
        self.user_id = user_id
        self.hero = hero
        self.stats = PlayerStats(hp, shield, speed, speed_length)
        self.sprite = char_sprite
