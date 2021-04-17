"""
Holds all the code to run the game itself
"""
import pygame
import pygame.freetype
from .bootstraper import BootStrap
from .assets import *
from twisted.internet import reactor
from .game import Game


class App:
    def __init__(self, boot_strap: BootStrap):
        self._run = True
        self.user = boot_strap
        self.state = 0  # 0: menu, 1: Lobby Code, 2: Game, 3: stats, 4: hero_picker 69: Error
        self.lobby_type = 0  # 0: nothing, 1: Create Lobby, 2: Enter Lobby Code
        self.error_message = None  # Stores error message if needed
        self.game = None  # Stores game object when in play
        self.clock = pygame.time.Clock()
        self.stats = None
        self.user_entry = ""  # Stores data entered by user
        # Start Display
        pygame.display.init()
        self._display = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)  # Creates display for the pygame window
        print(pygame.display.Info())
        # Starts Fonts
        pygame.freetype.init()
        self.font_bold_menu = pygame.freetype.Font("assets/Montserrat/Montserrat-Bold.ttf", 48)
        self.sub_font = pygame.freetype.Font("assets/Montserrat/Montserrat-Regular.ttf", 29)
        self._factory = None

    @property
    def websocket(self):
        if self._factory:
            return self._factory._protocol

    @staticmethod
    def __exit():
        """
        Exit Application
        :return: None
        """
        pygame.quit()
        reactor.stop()
        exit(0)

    def main_menu_display(self):
        """
        Displays Menu
        :return: None
        """
        self._display.fill(white)
        self.font_bold_menu.render_to(self._display, (48, 48), "Untitled online RPG", black)
        self.sub_font.render_to(self._display, (48, 100), f"User: {self.user.username}", black)
        # Join Lobby
        pygame.draw.rect(self._display, light_grey, join_lobby_rect)
        pygame.draw.rect(self._display, black, join_lobby_rect, 1)
        self.font_bold_menu.render_to(self._display, (823, 250), "Enter Lobby", black)
        # Create Lobby
        pygame.draw.rect(self._display, light_grey, create_lobby_rect)
        pygame.draw.rect(self._display, black, create_lobby_rect, 1)
        self.font_bold_menu.render_to(self._display, (792, 436), "Create Lobby", black)
        # View Stats
        pygame.draw.rect(self._display, light_grey, view_stats_rect)
        pygame.draw.rect(self._display, black, view_stats_rect, 1)
        self.font_bold_menu.render_to(self._display, (827, 630), "View Stats", black)
        # Exit
        pygame.draw.rect(self._display, light_grey, exit_main_menu_rect)
        pygame.draw.rect(self._display, black, exit_main_menu_rect, 1)
        self.font_bold_menu.render_to(self._display, (912, 825), "Exit", black)

    def main_menu_selector(self, mouse_pos):
        """
        Handles Main Menu input
        :return:
        """
        if join_lobby_rect.collidepoint(mouse_pos):
            print("join Lobby")
            self.lobby_type = 2
            self.hero_select_screen()
        elif create_lobby_rect.collidepoint(mouse_pos):
            print("create Lobby")
            self.lobby_type = 1
            self.hero_select_screen()
        elif view_stats_rect.collidepoint(mouse_pos):
            self.stats = self.user.get_profile()
            self.stats_display()
        elif exit_main_menu_rect.collidepoint(mouse_pos):
            self.__exit()

    def stats_display(self):
        if self.stats:
            self.state = 3
            self._display.fill(white)
            # Draw back button
            pygame.draw.rect(self._display, light_grey, return_to_rect)
            pygame.draw.rect(self._display, black, return_to_rect, 1)
            self.sub_font.render_to(self._display, (100, 980), "Return to Menu", black)
            # Display Stats
            profile = self.stats.get('profile')
            self.font_bold_menu.render_to(self._display, (1175, 378), "Stats", black)
            self.sub_font.render_to(self._display, (1175, 451), f"Games: {profile.get('games')}")
            self.sub_font.render_to(self._display, (1175, 500), f"Wins: {profile.get('wins')}")
            self.sub_font.render_to(self._display, (1175, 550), f"Loses: {profile.get('loses')}")
        else:
            self.error_display("Unable to get user stats")

    def stats_selector(self, mouse_pos):
        if return_to_rect.collidepoint(mouse_pos):
            self.state = 0

    def error_display(self, error_message: str):
        self.error_message = error_message
        self.state = 69
        self._display.fill(white)
        self.font_bold_menu.render_to(self._display, (48, 48), "Untitled online RPG", black)
        self.sub_font.render_to(self._display, (48, 100), f"User: {self.user.username}", black)
        self.font_bold_menu.render_to(self._display, (700, 436), f"Error: {self.error_message}", black)
        pygame.draw.rect(self._display, light_grey, exit_main_menu_rect)
        pygame.draw.rect(self._display, black, exit_main_menu_rect, 1)
        self.font_bold_menu.render_to(self._display, (912, 825), "Main Menu", black)

    def error_selector(self, mouse_pos):
        if exit_main_menu_rect.collidepoint(mouse_pos):
            self.state = 0
            self.main_menu_display()

    def hero_select_screen(self):
        self.state = 4
        self._display.fill(white)
        self.font_bold_menu.render_to(self._display, (48, 48), "Select your Hero", black)
        # Buttons
        pygame.draw.rect(self._display, light_grey, hero_1_rect)
        pygame.draw.rect(self._display, black, hero_1_rect, 1)
        self.font_bold_menu.render_to(self._display, (297, 915), "Gatron", black)
        pygame.draw.rect(self._display, light_grey, hero_2_rect)
        pygame.draw.rect(self._display, black, hero_2_rect, 1)
        self.font_bold_menu.render_to(self._display, (721, 915), "Sova", black)
        pygame.draw.rect(self._display, light_grey, hero_3_rect)
        pygame.draw.rect(self._display, black, hero_3_rect, 1)
        self.font_bold_menu.render_to(self._display, (1101, 915), "Ranger", black)

    def hero_select_selector(self, mouse_pos):
        hero = None
        if hero_1_rect.collidepoint(mouse_pos):
            hero = 1
        elif hero_2_rect.collidepoint(mouse_pos):
            hero = 2
        elif hero_3_rect.collidepoint(mouse_pos):
            hero = 3
        if hero:
            if self.lobby_type == 1:
                self.open_lobby(hero)
            elif self.lobby_type == 2:
                self.join_lobby(hero)

    def open_lobby(self, hero_id: int):
        """
        Open a game lobby
        :param hero_id:
        :return:
        """
        lobby_code = self.user.open_lobby(False)  # Open Lobby
        if lobby_code:  # Enter lobby state
            self.game = Game(lobby_code, self, hero_id)
            self.state = 2
            pass
            # TODO create game object
        else:  # If there's an error we go to the error screen
            self.error_display("Unable to open lobby")

    def join_lobby(self, hero_id: int):
        self.state = 1
        # TODO take in and Validate room code
        self.game = Game(self.user_entry, self, hero_id)
        pass

    def main(self):
        """
        Runs the pygame window
        :return: None
        """
        while self._run:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.state == 0:
                        self.main_menu_selector(event.pos)
                    elif self.state == 3:
                        self.stats_selector(event.pos)
                    elif self.state == 4:
                        self.hero_select_selector(event.pos)
                elif event.type == pygame.QUIT:
                    self.__exit()
            # Sets FPS display
            self.clock.tick(60)
            self.sub_font.render_to(self._display, (0, 0), f"FPS: {round(self.clock.get_fps(), 1)}", black)
            # Display appropriate screen
            if self.state == 0:
                self.main_menu_display()
            elif self.state == 3:
                self.stats_display()
            elif self.state == 4:
                self.hero_select_screen()
            elif self.state == 2:  # if we're in game we yield so that Twisted can run Websocket calls
                yield
            pygame.display.update()
