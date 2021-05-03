"""
Holds all the code to run the game itself
"""
import pygame
from .bootstraper import BootStrap
from .assets import *
from twisted.internet import reactor
from .game import Game
from .ws import URPGClientFactory
from .gameData import GameData
import json
from twisted.internet import ssl
from autobahn.twisted.websocket import connectWS
from .shared import draw_button


class App:
    def __init__(self, boot_strap: BootStrap):
        self._factory = None
        self._run = True
        self.user = boot_strap
        self.state = 0  # 0: menu, 1: Lobby Code, 2: Game, 3: stats, 4: hero_picker 69: Error
        self.lobby_type = 0  # 0: nothing, 1: Create Lobby, 2: Enter Lobby Code
        self.error_message = None  # Stores error message if needed
        self.game = None  # Stores game object when in play
        self.clock = pygame.time.Clock()
        self.stats = None
        self.user_entry = ""  # Stores data entered by user
        self.hero_id = None
        self.game_data = GameData(self.user.game_data)
        self.frame = None  # Stores next frame to show
        # Start Display
        pygame.display.init()
        pygame.display.set_caption('Untitled Online RPG')  # Set window name
        self.elapsed = pygame.time.get_ticks()
        self.display = pygame.display.set_mode((1920, 1080))  # Creates display for the pygame window
        self.elapsed = pygame.time.get_ticks()  # used to set animation speed checks
        print(pygame.display.Info())
        self.open_websocket()

    @property
    def websocket(self):
        """
        Get websocket
        :return: Websocket
        """
        if self._factory:
            return self._factory.client_protocol
        else:
            return None

    def __exit(self):
        """
        Exit Application
        :return: None
        """
        self._run = False
        self.websocket.sendClose()
        reactor.stop()

    def open_websocket(self):
        """
        Open Websocket
        :return: None
        """
        self._factory = URPGClientFactory(self.user.server, self, self.user.token, self.user.secure)
        # Checks if connection is secure
        if self._factory.isSecure:
            context_factory = ssl.ClientContextFactory()
        else:
            context_factory = None
        connectWS(self._factory, context_factory)  # Starts the Websocket connection
        reactor.connectTCP('127.0.0.1', self.user.port, self._factory)  # Start reactor

    def close_websocket(self):
        """
        Close websocket
        :return: None
        """
        if self.websocket:
            self.websocket.sendClose(1000)

    def ws_send_json(self, message: dict):
        """
        Send message via websocket
        :param message: message to send
        :return: None
        """
        payload = json.dumps(message, ensure_ascii=False).encode('utf8')
        self.websocket.sendMessage(payload)

    def back_to_menu(self):
        """
        Return to main menu
        :return: None
        """
        self.state = 0
        self.main_menu_display()
        self.game = None

    def main_menu_display(self):
        """
        Displays Menu
        :return: None
        """
        bold_48_font.render_to(self.display, (48, 48), "Untitled online RPG", black)
        regular_29_font.render_to(self.display, (48, 100), f"User: {self.user.username}", black)
        # Join Lobby
        draw_button(self.display, join_lobby_rect, "Enter Lobby")
        # Create Lobby
        draw_button(self.display, create_lobby_rect, "Create Lobby")
        # View Stats
        draw_button(self.display, view_stats_rect, "View Stats")
        # Exit
        draw_button(self.display, exit_main_menu_rect, "Exit")

    def main_menu_selector(self, mouse_pos):
        """
        Handles Main Menu input
        :return: None
        """
        if join_lobby_rect.collidepoint(mouse_pos):
            self.lobby_type = 2
            self.hero_select_screen()
        elif create_lobby_rect.collidepoint(mouse_pos):
            self.lobby_type = 1
            self.hero_select_screen()
        elif view_stats_rect.collidepoint(mouse_pos):
            self.stats = self.user.get_profile()
            self.stats_display()
        elif exit_main_menu_rect.collidepoint(mouse_pos):
            self.__exit()

    def stats_display(self):
        """
        Display the stats on screen
        :return: None
        """
        if self.stats:
            self.state = 3
            self.display.fill(white)
            # Draw back button
            draw_button(self.display, return_to_rect, "Return to Menu", small_font=True)
            # Display last hero
            if ((pygame.time.get_ticks() - self.elapsed) > 100) or self.frame is None:
                self.elapsed = pygame.time.get_ticks()
                self.frame = sprite_data[self.user.hero].animation_by_id["0"].get_next_frame
            self.display.blit(self.frame, (200, 250))
            # Display Stats
            profile = self.stats.get('profile')
            bold_48_font.render_to(self.display, (1175, 378), "Stats", black)
            regular_29_font.render_to(self.display, (1175, 451), f"Games: {profile.get('games')}")
            regular_29_font.render_to(self.display, (1175, 500), f"Wins: {profile.get('wins')}")
            regular_29_font.render_to(self.display, (1175, 550), f"Loses: {profile.get('loses')}")
        else:
            self.error_display("Unable to get user stats")

    def stats_selector(self, mouse_pos):
        """
        process inputs while on stats screen
        :param mouse_pos: mouse position
        :return: None
        """
        if return_to_rect.collidepoint(mouse_pos):  # Return to main menu
            self.state = 0

    def error_display(self, error_message: str or None):
        """
        Display Error
        :param error_message: error message to show
        :return: None
        """
        if error_message is not None:
            self.error_message = error_message
        self.state = 69
        self.display.fill(white)
        bold_48_font.render_to(self.display, (48, 48), "Untitled online RPG", black)
        regular_29_font.render_to(self.display, (48, 100), f"User: {self.user.username}", black)
        bold_48_font.render_to(self.display, (700, 436), f"Error: {self.error_message}", black)
        draw_button(self.display, exit_main_menu_rect, "Main Menu", small_font=True)

    def error_selector(self, mouse_pos):
        """
        process inputs while on error screen
        :param mouse_pos: mouse position
        :return: None
        """
        if exit_main_menu_rect.collidepoint(mouse_pos):
            self.state = 0
            self.main_menu_display()

    def hero_select_screen(self):
        """
        Display heroes available to select
        :return:
        """
        self.state = 4
        self.display.fill(white)
        bold_48_font.render_to(self.display, (48, 48), "Select your Hero", black)
        # Buttons
        draw_button(self.display, hero_1_rect, "Gatron")
        draw_button(self.display, hero_2_rect, "Maxmus")
        draw_button(self.display, hero_3_rect, "Boxer")
        # Show heroes on screen above buttons
        if ((pygame.time.get_ticks() - self.elapsed) > 100) or self.frame is None:
            self.elapsed = pygame.time.get_ticks()
            self.frame = pygame.Surface((1920, 1080), pygame.SRCALPHA, 32)
            self.frame.blit(sprite_data[1].animation_by_id["0"].get_next_frame, (15, 380))
            self.frame.blit(sprite_data[2].animation_by_id["0"].get_next_frame, (450, 300))
            self.frame.blit(sprite_data[3].animation_by_id["0"].get_next_frame, (960, 250))
            self.frame = self.frame.convert_alpha()
        self.display.blit(self.frame, (0, 0))

    def hero_select_selector(self, mouse_pos):
        """
        Process mouse input for hero select screen
        :param mouse_pos: mouse position
        :return: None
        """
        hero = None
        if hero_1_rect.collidepoint(mouse_pos):
            hero = 1
        elif hero_2_rect.collidepoint(mouse_pos):
            hero = 2
        elif hero_3_rect.collidepoint(mouse_pos):
            hero = 3
        if hero:
            self.user.update_hero(hero)
            if self.lobby_type == 1:
                self.hero_id = hero
                self.open_lobby()
            elif self.lobby_type == 2:
                self.hero_id = hero
                self.user_entry = ""
                self.join_lobby_display()

    def open_lobby(self):
        """
        Open a game lobby
        :return: None
        """
        lobby_code = self.user.open_lobby(False)  # Open Lobby
        if lobby_code:  # Enter lobby state
            self.game = Game(lobby_code, self, self.hero_id)
            self.state = 2
        else:  # If there's an error we go to the error screen
            self.error_display("Unable to open lobby")

    def join_lobby_display(self):
        """
        Join lobby screen
        :return: None
        """
        self.state = 1
        self.display.fill(white)
        bold_48_font.render_to(self.display, (48, 48), "Enter Lobby Code", black)
        # button
        draw_button(self.display, enter_lobby_rect, "Join Lobby")
        # txt box
        regular_18_font.render_to(self.display, (697, 474), "Enter Lobby Code", black)
        if (pygame.time.get_ticks() - self.elapsed) > 250:
            # This if statement is used to create a flashing cursor
            self.elapsed = pygame.time.get_ticks()
            bold_36_font.render_to(self.display, (697, 496), f"{self.user_entry}", black)
        else:
            bold_36_font.render_to(self.display, (697, 496), f"{self.user_entry}|", black)
        pygame.draw.rect(self.display, light_grey, (697, 540, 500, 3))

    def join_lobby_key_press(self, event):
        """
        process keyboard input for join lobby
        :param event: pygame event
        :return: None
        """
        if event.key == pygame.K_BACKSPACE:  # If backspace remove last char
            self.user_entry = self.user_entry[:-1]
        elif event.key == pygame.K_RETURN:  # If enter is pressed
            # enter game lobby
            if self.user.check_lobby_code(self.user_entry):
                self.game = Game(self.user_entry, self, self.hero_id)
                self.state = 2
            else:
                self.error_display("Invalid Room Code!")
        else:
            self.user_entry += event.unicode

    def join_lobby_selector(self, mouse_pos):
        """
        Process mouse input for join lobby
        :param mouse_pos: mouse position
        :return: None
        """
        if enter_lobby_rect.collidepoint(mouse_pos):
            if self.user.check_lobby_code(self.user_entry):
                self.game = Game(self.user_entry, self, self.hero_id)
                self.state = 2
            else:
                self.error_display("Invalid Room Code!")

    def main(self):
        """
        Runs the pygame window
        :return: None
        """
        # Note: You see so many if/elif statements as Python doesn't have switch/case statements, yes there's dict
        # but they can get messy with variables
        while self._run:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.state == 0:
                        self.main_menu_selector(event.pos)
                    elif self.state == 1:
                        self.join_lobby_selector(event.pos)
                    elif self.state == 2:
                        self.game.mouse_input_manager(event.pos)
                    elif self.state == 3:
                        self.stats_selector(event.pos)
                    elif self.state == 4:
                        self.hero_select_selector(event.pos)
                    elif self.state == 69:
                        self.error_selector(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if self.state == 1:
                        self.join_lobby_key_press(event)
                elif event.type == pygame.QUIT:
                    self.__exit()
            # Display appropriate screen
            self.display.fill(white)
            if self.state == 0:
                self.main_menu_display()
            elif self.state == 1:
                self.join_lobby_display()
            elif self.state == 3:
                self.stats_display()
            elif self.state == 4:
                self.hero_select_screen()
            elif self.state == 69:
                self.error_display(None)
            elif self.state == 2:
                self.game.main()
            # Sets FPS display
            self.clock.tick(60)
            regular_18_font.render_to(self.display, (5, 5), f"FPS: {round(self.clock.get_fps(), 1)}", black)
            pygame.display.update()
            yield
