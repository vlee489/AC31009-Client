from .player import Player, PlayerStats
from .gameData import GameData, HeroData, MoveData
from .characterSprite import AnimationSprite
from .assets import *
from .shared import draw_button
import pygame


class Game:
    """
    Actually runs the game itself when in a room/lobby
    """

    def __init__(self, room_code: str, app, hero_id: int):
        print(f"room code: {room_code}")
        self._app = app  # Stores ref back to the app the launches the Game object
        self.room_code = room_code  # Stores the room-code that needs sent back to the server per move execution
        # Queues
        self.messages = []  # Stores all the messages coming in via websockets
        self.moves = []  # Holds all the moves that need to be played out
        self.cg = []  # Holds all the character graphics that need to be played out still
        self.state = 0
        # 0 : Waiting on Response from server
        # 1 : Waiting on other player
        # 2 : Pick Move Type
        # 3 : Pick Attack
        # 4 : Pick Item
        # 5 : playing Move
        self.active = False  # If room is active
        # Store Player Data
        self.player_a = None
        self.player_b = None
        self.player_num = -1  # 0 = A, 1 = B  States which player we are
        self.action = None  # Stores the last action carried out and sent to server
        self.winner = None  # Stores the winner at the end of the game
        # Stores Sprites for player models
        self.button_rect = []  # Used to store where the rects are input checking
        # stores frames for each character, so they can be displayed again
        self.player_a_frame = None
        self.player_b_frame = None
        self.shown_ending = False
        # To stop audio repeating for move
        self.player_a_audio = False
        self.player_b_audio = False
        self.background = pygame.image.load("assets/bg/background.png")
        # Attempt to join room
        self.send_ws_json({
            "action": "join",
            "roomCode": room_code,
            "hero": {
                "id": hero_id
            }
        })

    @property
    def display(self) -> pygame.display:
        """
        Returns the pygame display
        :return: pygame.display
        """
        return self._app.display

    @property
    def game_data(self) -> GameData:
        """
        Return the game data object
        :return: GameData
        """
        return self._app.game_data

    @property
    def get_player_hero(self) -> HeroData:
        """
        Get the hero of the player
        :return: HeroData
        """
        if self.player_num == 0:
            return self.player_a.hero
        else:
            return self.player_b.hero

    @property
    def get_player_stats(self) -> PlayerStats:
        """
        Get the stats of the player
        :return: PlayerStats
        """
        if self.player_num == 0:
            return self.player_a.stats
        else:
            return self.player_b.stats

    @property
    def player_a_sprites(self) -> CharacterSprite:
        """
        Get Player a's sprites
        :return: CharacterSprite
        """
        return self.player_a.sprite

    @property
    def player_b_sprites(self) -> CharacterSprite:
        """
        Get Player b's sprites
        :return: CharacterSprite
        """
        return self.player_b.sprite

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
        """
        Display waiting joining message
        :return: None
        """
        bold_36_font.render_to(self.display, (691, 518), "Waiting for opponent to join", black)
        bold_48_font.render_to(self.display, (56, 48), "Lobby Code: ", black)
        regular_48_font.render_to(self.display, (370, 48), f"{self.room_code}", black)

    def display_stats(self):
        """
        Display stats on the
        :return: None
        """
        # calc player_a HP box length
        player_a_hp_width = int((self.player_a.stats.HP / self.player_a.hero.HP) * 500)
        player_b_hp_width = int((self.player_b.stats.HP / self.player_b.hero.HP) * 500)
        # Draw Player A Health
        bold_36_font.render_to(self.display, (22, 34), "HP", black)
        pygame.draw.rect(self.display, white, (86, 30, 500, 35))
        pygame.draw.rect(self.display, (green if (self.player_a.stats.HP / self.player_a.hero.HP) > 0.5 else damage_red)
                         , (86, 30, player_a_hp_width, 35))
        pygame.draw.rect(self.display, black, (86, 30, 500, 35), 1)
        regular_20_font.render_to(self.display, (100, 36), f"{self.player_a.stats.HP}/{self.player_a.hero.HP}", black)
        # Draw Player B Health
        bold_36_font.render_to(self.display, (1848, 34), "HP", black)
        pygame.draw.rect(self.display, white, (1333, 30, 500, 35))
        pygame.draw.rect(self.display, (green if (self.player_b.stats.HP / self.player_b.hero.HP) > 0.5 else damage_red)
                         , ((1333 + (500 - player_b_hp_width)), 30, player_b_hp_width, 35))
        pygame.draw.rect(self.display, black, (1333, 30, 500, 35), 1)
        # Work out where to put the hp text from the right
        player_b_hp_width = 1820 - (regular_20_font.get_rect(f"{self.player_b.stats.HP}/{self.player_b.hero.HP}")[2])
        regular_20_font.render_to(self.display, (player_b_hp_width, 36),
                                  f"{self.player_b.stats.HP}/{self.player_b.hero.HP}", black)
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
        """
        Display move type buttons
        :return: None
        """
        # Attack Box
        draw_button(self.display, attack_move_rect, "Attack")
        # item box
        draw_button(self.display, item_move_rect, "Use Item")
        # Shield Box
        # get is player has shield and grey out if they don't
        if self.get_player_stats.shield <= 0:
            draw_button(self.display, shield_rect, "Shield", disabled=True)
        else:
            draw_button(self.display, shield_rect, "Shield")
        # Skip Box
        draw_button(self.display, skip_rect, "Skip")

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
        elif shield_rect.collidepoint(mouse_pos):
            if self.get_player_stats.shield > 0:  # Only trigger if player has shields to use
                self.send_ws_json({
                    "action": "move",
                    "roomCode": self.room_code,
                    "move": {
                        "moveType": 2,
                        "id": 0
                    }
                })
        elif skip_rect.collidepoint(mouse_pos):
            self.send_ws_json({
                "action": "move",
                "roomCode": self.room_code,
                "move": {
                    "moveType": 3,
                    "id": 0
                }
            })

    def display_wait_for_opponent(self):
        """
        Display wait for opponent
        :return: None
        """
        bold_64_font.render_to(self.display, (570, 920), "Waiting on opponent....", light_grey)

    def display_back_button(self):
        """
        Displays back button
        :return: None
        """
        pygame.draw.rect(self.display, light_grey, back_button_rect)
        pygame.draw.rect(self.display, black, back_button_rect, 1)
        self.display.blit(back_icon, (119, 908))

    def display_attacks(self):
        """
        Works on displaying the buttons for attacks
        :return: None
        """
        self.button_rect = []  # Empty array
        # Display back button
        self.display_back_button()
        hero = self.get_player_hero
        start_x = 275
        for attack in hero.moves:  # For each attack a hero can make
            working_rect = Rect(start_x, 890, 350, 120)  # This is where out button should go
            self.button_rect.append({
                "rect": working_rect,
                "move_id": attack.ID,
                "move_type": 0  # 0: attack, 1: item, 2:shield, 3: skip
            })
            draw_button(self.display, working_rect, attack.name)
            start_x += 404  # Set location of next button

    def display_items(self):
        """
        Displays items that can be used
        :return: None
        """
        self.button_rect = []  # Empty array
        # Display back button
        self.display_back_button()
        start_x = 275
        for item in self.game_data.items:
            working_rect = Rect(start_x, 890, 350, 120)  # This is where out button should go
            self.button_rect.append({
                "rect": working_rect,
                "move_id": item.ID,
                "move_type": 1  # 0: attack, 1: item, 2:shield, 3: skip
            })
            draw_button(self.display, working_rect, item.name)
            start_x += 404  # Set location of next button

    def move_input(self, mouse_pos):
        """
        Process input for when move being selected
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

    def display_winner(self):
        """
        Display winner
        :return: None
        """
        if self.winner == self.player_num:
            message = "You are the winner!"
        elif self.winner == 2:
            message = "Game Draw!"
        else:
            message = "You've Lost!"
        message_x = 962 - ((bold_48_font.get_rect(f"{message}")[2]) // 2)
        bold_48_font.render_to(self.display, (message_x, 60), f"{message}", black)
        # Draw back button
        draw_button(self.display, return_to_rect, "Return to Menu", small_font=True)

    def move_processor(self):
        """
        Turns the moves into cg (character graphics) movements
        :return: None
        """
        hero_move: MoveData
        player_sprite: CharacterSprite
        opponent = -1
        opponent_animation = None
        for x in range(len(self.moves)):
            move = self.moves.pop(0)
            if move["move"]["moveType"] == 0:
                if move["player"] == 0:
                    move_player_hero: HeroData = self.player_a.hero
                    move_player_sprite = self.player_a_sprites
                    if self.player_b.stats.get_hp_diff > 0:  # If player takes a hit
                        opponent_animation = self.player_b_sprites.animation_by_id[f"-1"]  # Get damage animation
                        opponent = 1
                else:
                    move_player_hero: HeroData = self.player_b.hero
                    move_player_sprite = self.player_b_sprites
                    if self.player_a.stats.get_hp_diff > 0:  # If player takes a hit
                        opponent_animation = self.player_a_sprites.animation_by_id[f"-1"]  # Get damage animation
                        opponent = 0
                for hero_move in move_player_hero.moves:  # for moves hero has
                    if hero_move.ID == move["move"]["id"]:  # if the move we're looking at and hero move are the same
                        animation = move_player_sprite.animation_by_id[f"{hero_move.animation}"]
                        self.cg.append(AnimationSprite(animation, move["player"], hero_move.animation))
                        if opponent_animation is not None:
                            self.cg.append(AnimationSprite(opponent_animation, opponent, -100))

    def cg_player(self):
        """
        Plays out all the character movement on the surface
        :return: None
        """
        # Only run animations ever 150ms
        if (pygame.time.get_ticks() - self._app.elapsed) > 150:
            self._app.elapsed = pygame.time.get_ticks()
            self.player_a_frame = None
            self.player_b_frame = None
            if len(self.cg) > 0:
                move_cg: AnimationSprite = self.cg[0]
                if move_cg.player == 0:
                    self.player_a_frame = move_cg.animation.get_next_frame
                    if move_cg.audio > -100 and not self.player_a_audio:  # has audio to play and not been played
                        self.player_a_audio = True
                        audio_data[self.player_a.hero.ID].audio_by_id[f"{move_cg.audio}"].play()
                elif move_cg.player == 1:
                    self.player_b_frame = move_cg.animation.get_next_frame
                    if move_cg.audio > -100 and not self.player_b_audio:  # has audio to play and not been played
                        self.player_b_audio = True
                        audio_data[self.player_b.hero.ID].audio_by_id[f"{move_cg.audio}"].play()
                # if played through, remove frame from cg list
                if move_cg.animation.animation_played_through:
                    self.cg.pop(0)
        # if no moves to be shown and end of the game and death animation hasn't been shown
        if (self.winner is not None) and (not self.shown_ending) and (len(self.cg) == 0):
            if self.winner == 0:
                loser_animation_id = self.player_b.hero.death_animation
                self.player_b_frame = self.player_b_sprites.animation_by_id[f"{loser_animation_id}"].get_next_frame
                if self.player_b_sprites.animation_by_id[f"{loser_animation_id}"].animation_played_through:
                    self.shown_ending = True
            if self.winner == 1:
                loser_animation_id = self.player_a.hero.death_animation
                self.player_a_frame = self.player_a_sprites.animation_by_id[f"{loser_animation_id}"].get_next_frame
                if self.player_a_sprites.animation_by_id[f"{loser_animation_id}"].animation_played_through:
                    self.shown_ending = True
        # if no animation is assigned, set the next frame of the idle animation
        if self.player_a_frame is None:
            self.player_a_frame = self.player_a_sprites.animation_by_id["0"].get_next_frame
        if self.player_b_frame is None:
            self.player_b_frame = self.player_b_sprites.animation_by_id["0"].get_next_frame
        # Calculate where sprite should go on window
        a_y_loc = 950 - self.player_a_frame.get_height()
        b_y_loc = 950 - self.player_b_frame.get_height()
        b_x_loc = 1920 - (10 + self.player_b_frame.get_width())
        # Display frame
        self.display.blit(self.player_a_frame, (10, a_y_loc))
        flip_b = pygame.transform.flip(self.player_b_frame, True, False)  # Flip Player B
        self.display.blit(flip_b, (b_x_loc, b_y_loc))

    def display_move_info(self, move_id: int):
        """
        Display data on a move on screen
        :param move_id: move ID
        :return: None
        """
        move_data = None
        for move in self.get_player_hero.moves:
            if move.ID == move_id:
                move_data = move
                break
        if move_data:  # if there's data to show, we display the data
            pygame.draw.rect(self.display, info_box_grey, (1474, 870, 420, 200))
            bold_48_font.render_to(self.display, (1494, 890), f"{move_data.name}")
            regular_18_font.render_to(self.display, (1494, 940), f"{move_data.description}")
            bold_18_font.render_to(self.display, (1494, 970), f"Damage: ")
            regular_18_font.render_to(self.display, (1594, 970), f"{move_data.HP}")
            bold_18_font.render_to(self.display, (1494, 995), f"Recoil: ")
            regular_18_font.render_to(self.display, (1594, 995), f"{move_data.recoil}")
            bold_18_font.render_to(self.display, (1494, 1020), f"Speed: ")
            regular_18_font.render_to(self.display, (1594, 1020), f"{move_data.speed}")

    def display_item_info(self, item_id: int):
        """
        Display data on a item on screen
        :param item_id: item ID
        :return: None
        """
        item = self.game_data.items_by_id.get(f"{item_id}")
        if item:
            pygame.draw.rect(self.display, info_box_grey, (1474, 870, 420, 200))
            bold_48_font.render_to(self.display, (1494, 890), f"{item.name}")
            regular_18_font.render_to(self.display, (1494, 940), f"{item.description}")
            start_x = 970
            for affect in item.affect_display:
                bold_18_font.render_to(self.display, (1494, start_x), f"{affect[0]}: ")
                regular_18_font.render_to(self.display, (1594, start_x), f"{affect[1]}")
                start_x += 25

    def hover_over_info(self):
        """
        Checks if the user's mouse is hovering over a button
        :return: None
        """
        if self.state == 3 or self.state == 4:
            for rect in self.button_rect:
                if rect['rect'].collidepoint(pygame.mouse.get_pos()):
                    if rect['move_type'] == 0:  # If hovering over a move button display details on the move
                        self.display_move_info(rect["move_id"])
                    elif rect['move_type'] == 1:  # If over a item button show details on the item
                        self.display_item_info(rect['move_id'])

    def mouse_input_manager(self, mouse_pos):
        """
        Process Mouse input for game
        :param mouse_pos: mouse position
        :return: None
        """
        if self.state == 2:
            self.move_type_input(mouse_pos)
        elif self.state == 3 or self.state == 4:
            self.move_input(mouse_pos)
        elif (not self.active) and (self.winner is not None):
            if return_to_rect.collidepoint(mouse_pos):
                self._app.back_to_menu()

    def main(self):
        """
        Runs the game event loop to display UI and process inputs
        :return: None
        """
        self.display.blit(self.background, (0, 0))
        if (self.active or self.winner is not None) and not self.shown_ending:
            self.cg_player()
            self.move_processor()
        # We don't display stuff for state 0 as it usually changes in a split second after server responds
        if not self.active:
            if self.winner is not None:
                self.display_winner()
            else:
                self.display_waiting_on_join()
        elif self.state == 1:
            self.display_wait_for_opponent()
        elif self.state == 2:
            self.display_move_type()
        elif self.state == 3:
            self.display_attacks()
        elif self.state == 4:
            self.display_items()
        elif self.state == 5:
            self.state = 2
        if self.active:  # If active display stats and check if user is ove rover button to give info
            self.hover_over_info()
            self.display_stats()
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
                                           player_a["shield"], player_a["speed"], player_a["speedLength"],
                                           sprite_data[player_a['heroID']])
                    player_b = message["status"]["playerB"]
                    self.player_b = Player(player_b["playerUsername"], player_b["playerID"],
                                           self.game_data.heroes_by_id[f"{player_b['heroID']}"], player_b["HP"],
                                           player_b["shield"], player_b["speed"], player_b["speedLength"],
                                           sprite_data[player_b['heroID']])
                    # Work out the player we are
                    if player_a["playerID"] == self._app.user.ID:
                        self.player_num = 0
                    elif player_b["playerID"] == self._app.user.ID:
                        self.player_num = 1
                    else:
                        raise LookupError("User isn't either player")  # Throw an error is we're neither player
                    self.state = 2
                if message['reply'] == "round":  # If new round data sent over
                    self.moves = self.moves + message["moves"]  # Place the moves to be shown into the array
                    player_a = message["playerA"]
                    self.player_a.stats.set_stats(player_a['HP'], player_a['shield'],
                                                  player_a["speed"], player_a["speedLength"])
                    player_b = message['playerB']
                    self.player_b.stats.set_stats(player_b['HP'], player_b['shield'],
                                                  player_b["speed"], player_b["speedLength"])
                    self.active = message['active']
                    if message["winner"] != "None":
                        self.winner = message["winner"]
                    self.player_a_audio = False
                    self.player_b_audio = False
                    self.state = 5
