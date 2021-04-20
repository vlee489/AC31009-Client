from .gameData import HeroData


class PlayerStats:
    """
    Stores data of players character and their current stats
    """

    def __init__(self, HP: int, shield: int, speed: int, speed_length: int):
        self.HP = HP
        self.shield = shield
        self.speed = speed
        self.speed_length = speed_length


class Player:
    """
    Stores data on a player
    """
    hero: HeroData

    def __init__(self, username: str, user_id: str, hero: HeroData,
                 hp: int, shield: int, speed: int, speed_length: int):
        self.username = username
        self.user_id = user_id
        self.hero = hero
        self.stats = PlayerStats(hp, shield, speed, speed_length)
