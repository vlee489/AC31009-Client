import requests
import os
import json
from pathlib import Path
import sys


def get_user_data_dir(app_name: str):
    """
    Get user Application Data storage location
    from: https://stackoverflow.com/questions/19078969/python-getting-appdata-folder-in-a-cross-platform-way
    :param app_name: name of application
    :return: str: application storage dir
    """
    if sys.platform == "win32":
        import winreg
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"
        )
        dir_, _ = winreg.QueryValueEx(key, "Local AppData")
        ans = Path(dir_).resolve(strict=False)
    elif sys.platform == 'darwin':
        ans = Path('~/Library/Application Support/').expanduser()
    else:
        ans = Path(os.getenv('XDG_DATA_HOME', "~/.local/share")).expanduser()
    return ans.joinpath(app_name)


class BootStrap:
    """
    Handles all storage and tasks for communicating with the server's REST api
    """

    def __init__(self, server: str, version: str, port: int):
        """
        Default constructor
        :param server: server link
        :param version: version number
        """
        self.dataDir = f"{get_user_data_dir('AC31009-Untitled-RPG')}/storage.json"
        self.server = server
        self.version = version
        self.port = port
        print(self.dataDir)
        if not os.path.isfile(self.dataDir):
            self.__createStorage__()
        with open(self.dataDir, "r") as dataFile:
            data = json.load(dataFile)
            self.token = data.get("token")
            self.username = data.get("username")
            self.ID = data.get("ID")
            self.game_data = data.get("gameData")
        self.check_game_data()
        # Run game version checks
        if self.version != self.game_data['clientSupport']:
            raise ValueError("Outdated client")

    def __createStorage__(self):
        """
        Creates the local storage file for the game
        :return: None
        """
        game_data_request = requests.get(f"http://{self.server}/gameData")
        if game_data_request.status_code != 200:
            raise ConnectionError("Unable to get server game Data")
        else:
            game_data = game_data_request.json()
        settings = {
            "gameVersion": self.version,
            "gameData": game_data,
            "token": "",
            "username": "",
            "ID": "",
        }
        if not os.path.isdir(get_user_data_dir('AC31009-Untitled-RPG')):
            os.mkdir(get_user_data_dir('AC31009-Untitled-RPG'))
        with open(self.dataDir, 'w+') as dataFile:
            json.dump(settings, dataFile, indent=4)

    def check_game_data(self):
        """
        Checks the local game data file with the one on the server
        :return: None
        """
        game_data_request = requests.get(f"http://{self.server}/gameData")
        if game_data_request.status_code != 200:
            raise ConnectionError("Unable to get server game Data")
        game_data = game_data_request.json()
        if self.game_data["version"] != game_data["version"]:
            self.game_data = game_data

    def update_storage_file(self):
        """
        Updates storage file
        :return: None
        """
        settings = {
            "gameVersion": self.version,
            "gameData": self.game_data,
            "token": self.token,
            "username": self.username,
            "ID": self.ID,
        }
        with open(self.dataDir, 'w+') as dataFile:
            json.dump(settings, dataFile, indent=4)

    def validate_token(self) -> bool:
        """
        Validate if stored token is valid
        :return: If token is valid or not
        """
        if self.token:
            response = requests.post(f"http://{self.server}/validateToken", data={
                "token": self.token,
            })
            if (response.status_code == 401) or (response.status_code != 200):
                self.token = ""
                return False
            elif response.status_code == 200 and response.json()["success"]:
                return True
        self.token = ""
        self.update_storage_file()
        return False

    def login(self, email: str, password: str):
        """
        Login a user
        :param email: User's email
        :param password: User's password
        :return: boolean is successful or not
        """
        self.token = ""
        self.ID = ""
        self.username = ""
        response = requests.post(f"http://{self.server}/login", data={
            "email": email,
            "password": password
        })
        if response.status_code == 401:
            return False
        reply = response.json()
        if reply["success"]:
            self.token = reply['token']
            self.ID = reply["details"]["ID"]
            self.username = reply["details"]["username"]
            self.update_storage_file()
            return True
        return False

    def get_profile(self):
        """
        Gets the user's profile
        :return: dict or bool
        """
        if not self.token:
            return False
        response = requests.get(f"http://{self.server}/profile", headers={
            "Authorization": self.token
        })
        if response.status_code != 200:
            return False
        else:
            return response.json()

    def open_lobby(self, public: bool):
        """
        Request the server to open a game lobby
        :param public: Public Lobby
        :return: False or roomCode
        """
        response = requests.post(f"http://{self.server}/openLobby", data={
            "open": public,
        }, headers={
            "Authorization": self.token
        })
        if response.status_code != 200:
            return False
        data = response.json()
        if data['success']:
            return data['roomCode']

    def check_lobby_code(self, room_code: str) -> bool:
        """
        Check if room_code is valid
        :param room_code: room code to check
        :return: if room is open and ready to be entered
        """
        response = requests.post(f"http://{self.server}/checkRoomCode", data={
            "roomCode": room_code,
        }, headers={
            "Authorization": self.token
        })
        if response.status_code == 200:
            return True
        elif response.status_code == 403:
            return False
        else:
            raise Exception("Remote Server Error")

