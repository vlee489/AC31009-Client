from .player import Player
from .assets import *
import pygame


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
        # 6 : playing Move
        self.state = 0
        self.active = False
        # Store Player Data
        self.player_a = None
        self.player_b = None
        self.player_num = -1  # 0 = A, 1 = B  States which player we are
        self.action = None
        # Attempt to join room
        self.send_ws_json({
            "action": "join",
            "roomCode": room_code,
            "hero": {
                "id": hero_id
            }
        })
        self.button_rect = []  # Used to store where the rects are input checking

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

    @property
    def get_player_hero(self):
        """
        Get the hero of the player
        :return: gameData.HeroData
        """
        if self.player_num == 0:
            return self.player_a.hero
        else:
            return self.player_b.hero

    def send_ws_json(self, message: dict):
        """
        send message via websocket
        :param message:
        :return: None
        """
        if 'action' in message:
            self.action = message['action']  # Set the action
            self._app.ws_send_json(message)
            self.state = 0  # Set state to wait for server

    def display_waiting_on_join(self):
        bold_36_font.render_to(self.display, (691, 518), "Waiting for opponent to join", black)
        bold_48_font.render_to(self.display, (56, 48), "Lobby Code: ", black)
        regular_48_font.render_to(self.display, (370, 48), f"{self.room_code}", black)

    def display_stats(self):
        """
        Display stats on the
        :return: None
        """
        # calc player_a HP box length
        player_a_hp_width = (self.player_a.stats.HP // self.player_a.hero.HP) * 500
        player_b_hp_width = (self.player_b.stats.HP // self.player_b.hero.HP) * 500
        # Draw Player A Health
        bold_36_font.render_to(self.display, (22, 34), "HP", black)
        pygame.draw.rect(self.display, green, (86, 30, player_a_hp_width, 35))
        pygame.draw.rect(self.display, black, (86, 30, 500, 35), 1)
        # Draw Player B Health
        bold_36_font.render_to(self.display, (1848, 34), "HP", black)
        pygame.draw.rect(self.display, green, ((1333 + (500 - player_b_hp_width)), 30, player_a_hp_width, 35))
        pygame.draw.rect(self.display, black, (1333, 30, 500, 35), 1)
        # Draw Player A Shields
        bold_36_font.render_to(self.display, (22, 84), "Shield", black)
        start_a_x_cord = 147
        for x in range(self.player_a.stats.shield):  # Draws the shield player has
            pygame.draw.rect(self.display, blue, (start_a_x_cord, 84, 100, 35))
            start_a_x_cord += 113
        start_a_x_cord = 147
        for x in range(self.player_a.hero.shield):  # draws the outlines for all shield available
            pygame.draw.rect(self.display, black, (start_a_x_cord, 84, 100, 35), 1)
            start_a_x_cord += 113
        # Draw Player B Shields
        bold_36_font.render_to(self.display, (1784, 84), "Shield", black)
        start_b_x_cord = 1670
        for x in range(self.player_b.stats.shield):  # Draws the shield player has
            pygame.draw.rect(self.display, blue, (start_b_x_cord, 84, 100, 35))
            start_b_x_cord -= 113
        start_b_x_cord = 1670
        for x in range(self.player_b.hero.shield):  # draws the outlines for all shield available
            pygame.draw.rect(self.display, black, (start_b_x_cord, 84, 100, 35), 1)
            start_b_x_cord -= 113
        # Display Usernames
        regular_29_font.render_to(self.display, (22, 130), f"{self.player_a.username}", black)
        p_b_width = regular_29_font.get_rect(f"{self.player_b.username}")[2]  # Used to work our right offset
        regular_29_font.render_to(self.display, ((1900 - p_b_width), 130), f"{self.player_b.username}", black)

    def display_move_type(self):
        # Attack Box
        pygame.draw.rect(self.display, light_grey, attack_move_rect)
        pygame.draw.rect(self.display, black, attack_move_rect, 1)
        bold_48_font.render_to(self.display, (498, 940), "Attack", black)
        # item box
        pygame.draw.rect(self.display, light_grey, item_move_rect)
        pygame.draw.rect(self.display, black, item_move_rect, 1)
        bold_48_font.render_to(self.display, (880, 940), "Use Item", black)
        # Skip Box
        pygame.draw.rect(self.display, light_grey, skip_rect)
        pygame.draw.rect(self.display, black, skip_rect, 1)
        bold_48_font.render_to(self.display, (1328, 940), "Skip", black)

    def move_type_input(self, mouse_pos):
        """
        Process mouse input for move type input display
        :param mouse_pos:
        :return: None
        """
        if attack_move_rect.collidepoint(mouse_pos):
            self.state = 3
        elif item_move_rect.collidepoint(mouse_pos):
            self.state = 4
        elif skip_rect.collidepoint(mouse_pos):
            pass

    def display_wait_for_opponent(self):
        bold_64_font.render_to(self.display, (570, 920), "Waiting on opponent....", black)

    def display_back_button(self):
        """
        Displays back button
        :return: None
        """
        pygame.draw.rect(self.display, light_grey, back_button_rect)
        pygame.draw.rect(self.display, black, back_button_rect, 1)

    def display_attacks(self):
        """
        Works on displaying the buttons for attacks
        :return: None
        """
        self.button_rect = []  # Empty array
        # Display back button
        self.display_back_button()
        hero = self.get_player_hero()
        start_x = 275
        for attack in hero.moves:  # For each attack a hero can make
            working_rect = Rect(start_x, 890, 350, 120)  # This is where out button should go
            self.button_rect.append({
                "rect": working_rect,
                "move_id": attack.ID,
                "move_type": 0  # 0: attack, 1: item, 2:shield, 3: skip
            })
            # Work out where the text will go
            attack_name_width = bold_48_font.get_rect(f"{attack.name}")[2]
            text_x = (start_x + 175) - (attack_name_width // 2)
            # Display button
            pygame.draw.rect(self.display, light_grey, working_rect)
            pygame.draw.rect(self.display, black, working_rect, 1)
            bold_48_font.render_to(self.display, (text_x, 928), f"{attack.name}", black)
            start_x += 404  # Set location of next button
            pass

    def attack_input(self, mouse_pos):
        """
        Process input for when attacks being selected
        :param mouse_pos: Mouse Location
        :return: None
        """
        for rect in self.button_rect:
            if rect['rect'].collidepoint(mouse_pos):
                self.send_ws_json({
                    "action": "move",
                    "roomCode": self.room_code,
                    "move": {
                        "moveType": rect['move_type'],
                        "id": rect['move_id']
                    }
                })
                break
        if back_button_rect.collidepoint(mouse_pos):
            # If back button is pressed, go back to the move type select screen
            self.state = 2


    def mouse_input_manager(self, mouse_pos):
        """
        Process Mouse input for game
        :param mouse_pos: mouse position
        :return: None
        """
        if self.state == 2:
            self.move_type_input(mouse_pos)
        elif self.state == 3:
            self.attack_input(mouse_pos)

    def main(self):
        """
        Runs the game event loop to display UI and process inputs
        :return: None
        """
        if self.active:
            self.display_stats()
            # We don't display stuff for state 0 as it usually changes in a split second after server responds
            if self.state == 1:
                self.display_wait_for_opponent()
            elif self.state == 2:
                self.display_move_type()
            elif self.state == 3:
                self.display_attacks()
        else:
            self.display_waiting_on_join()
        # Process messages in queue
        for x in range(len(self.messages)):
            message = self.messages.pop(0)  # first message in queue
            print(message)
            if "action" in message:  # If action
                if (message['action'] == self.action) and self.state == 0:
                    if (self.action in ["join", "move"]) and message['success']:
                        print(f"Server Responded to {self.action}")
                        self.state = 1  # state we're waiting for the other player to make their move
                    elif (not message['success']) and (message['action'] == "join"):
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
                    self.state = 2
