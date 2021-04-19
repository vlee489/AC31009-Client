from .player import Player


class Game:
    """
    Actually runs the game itself when in a room/lobby
    """
    def __init__(self, room_code: str, app, hero_id: int):
        self.room_code = room_code
        self.messages = []  # Stores all the messages coming in via websockets
        self._app = app  # Stores ref back to the app the launches the Game object
        # 0 : Waiting on Response
        # 1 : Waiting on other player
        # 2 : Pick Move Type
        # 3 : Pick Attack
        # 4 : Pick Item
        # 5 : waiting on player
        self.state = 0
        self.active = False
        # Store Player Data
        self.player_a = None
        self.player_b = None
        self.player_num = -1  # 0 = A, 1 = B  States which player we are
        # Attempt to join room
        self.send_ws_json({
            "action": "join",
            "roomCode": room_code,
            "hero": {
                "id": hero_id
            }
        })
        self.action = "join"  # Stores the last action sent via websockets

    @property
    def display(self):
        """
        Returns the pygame display
        :return: pygame.display
        """
        return self._app.display

    @property
    def game_data(self):
        """
        Return the game data object
        :return: classes.gameData.GameData
        """
        return self._app.game_data

    def send_ws_json(self, message: dict):
        """
        send message via websocket
        :param message:
        :return: None
        """
        self._app.ws_send_json(message)

    def main(self, events):
        # Process messages in queue
        for x in range(len(self.messages)):
            message = self.messages.pop(0)  # first message in queue
            print(message)
            if "action" in message:  # If action
                if (message['action'] == self.action) and self.state == 0:
                    if (self.action in ["join", "move"]) and message['success']:
                        self.state = 1  # state we're waiting for the other player to make their move
                    if (not message['success']) and (message['action'] == "join"):
                        # issue joining room, show an error in game
                        self._app.error_display(f"Unable to enter room: {message['message']}")
            elif "reply" in message:  # If it's a reply from server
                if message['reply'] == "start":  # Start the game, we process the messages
                    self.active = message["status"]["active"]  # Set game to active
                    # Assign the data for each player
                    player_a = message["status"]["playerA"]
                    self.player_a = Player(player_a["playerUsername"], player_a["playerID"],
                                           self.game_data.heroes_by_id[f"{player_a['heroID']}"], player_a["HP"],
                                           player_a["shield"], player_a["speed"], player_a["speedLength"])
                    player_b = message["status"]["playerB"]
                    self.player_b = Player(player_b["playerUsername"], player_b["playerID"],
                                           self.game_data.heroes_by_id[f"{player_b['heroID']}"], player_b["HP"],
                                           player_b["shield"], player_b["speed"], player_b["speedLength"])
                    # Work out the player we are
                    if player_a["playerID"] == self._app.user.ID:
                        self.player_num = 0
                    elif player_b["playerID"] == self._app.user.ID:
                        self.player_num = 1
                    else:
                        raise LookupError("User isn't either player")  # Throw an error is we're neither player
