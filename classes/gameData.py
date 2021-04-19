"""
Holds all the game data for characters, moves and items
"""


class MoveData:
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


class HeroData:
    """
    Stores data of players character
    """
    def __init__(self, ID: int, name: str, description: str, HP: int, shield: int, moves: list):
        self.ID = ID
        self.name = name
        self.description = description
        self.HP = HP
        self.shield = shield
        self.moves = moves


class StatData:
    def __init__(self, ID: int, name: str):
        self.ID = ID
        self.name = name


class ItemData:
    def __init__(self, ID: int, name: str, description: str, affects: list):
        self.ID = ID
        self.name = name
        self.description = description
        self.affects = affects


class GameData:
    def __init__(self, game_data: dict):
        self.heroes = []
        self.heroes_by_id = {}
        self.items = []
        self.items_by_id = {}
        self.stats = []
        self.stats_by_id = {}
        # Go through and load Hero data
        for hero in game_data['heros']:
            moves = []
            for attack in hero['attacks']:
                moves.append(MoveData(attack["id"], attack["name"], attack["description"], attack["HPDamage"],
                                      attack["recoil"], attack["speed"]))
            working_hero = HeroData(hero["id"], hero["name"], hero["description"],
                                    hero["health"], hero["shields"], moves)
            self.heroes.append(working_hero)
            self.heroes_by_id[f"{hero['id']}"] = working_hero
        # Go through items
        for item in game_data["items"]:
            affects = []
            for affect in item["affect"]:
                affects.append(StatData(affect['status'], affect['edit']))
            working_item = ItemData(item["id"], item["name"], item["description"], affects)
            self.items.append(working_item)
            self.items_by_id[f"{item['id']}"] = working_item
        # Go through Stats
        for stat in game_data["stats"]:
            working_stat = StatData(stat["id"], stat["name"])
            self.stats.append(working_stat)
            self.stats_by_id[stat["id"]] = working_stat
