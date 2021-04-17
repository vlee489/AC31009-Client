"""
All the classes for Game, Player, Hero and Moves
"""


class Move:
    """
    Stores data on moves
    """
    def __init__(self, ID: int, name: str, description: str, HP: int, recoil: int, speed: int):
        self.ID = ID
        self.name = name
        self.description = description
        self.HP = HP
        self.recoil = recoil
        self.speed = speed


class Hero:
    """
    Stores data of players character and their current stats
    """
    def __init__(self, ID: int, name: str, description: str, HP: int, shield: int, moves: list):
        self.ID = ID
        self.name = name
        self.description = description
        self.HP = HP
        self.shields = shield
        self.moves = moves


class Player:
    """
    Stores data on a player
    """
    def __init__(self, username: str, user_id: str, hero: Hero):
        self.username = username
        self.user_id = user_id
        self.hero = hero


class Game:
    def __init__(self, room_code: str, app, hero_id: int):
        self.room_code = room_code
        self.messages = []  # Stores all the messages coming in via websockets
        self._app = app
