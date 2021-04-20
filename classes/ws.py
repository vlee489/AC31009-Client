"""
Handles all the websocket stuff with Twisted & autobahn extended classes

This is based off the Websocket Pygame demo by globophobe
https://github.com/globophobe/pygame-websockets
"""
from autobahn.twisted.websocket import (
    WebSocketClientProtocol, WebSocketClientFactory
)
import json
from .game import Game


class URPGClientProtocol(WebSocketClientProtocol):
    def onOpen(self):
        """
        Open Websocket
        :return: None
        """
        print('WebSocket connection open.')
        self.factory._protocol = self  # Set factory protocol as a ref back to itself

    def onMessage(self, payload, is_binary):
        """
        Configures what happens when a new message comes via WS
        :param payload:
        :param is_binary:
        :return: None
        """
        if is_binary:
            # Server should never respond in binary
            raise ValueError("Server sent invalid message")
        data = json.loads(payload.decode('utf8'))  # Server sends JSON string, so we parse it into a dict to use
        if isinstance(self.factory.app.game, Game):
            # If the game is active and there's a game object, we append the WS message, else ignore it
            self.factory.app.game.messages.append(data)

    def onClose(self, was_clean, code, reason):
        """
        Runs on WS connection close
        :param was_clean:
        :param code:
        :param reason:
        :return: None
        """
        print('WebSocket connection closed: {0}'.format(reason))
        self.factory._protocol = None


class URPGClientFactory(WebSocketClientFactory):
    protocol = URPGClientProtocol

    def __init__(self, url: str, app, token: str):
        """
        Connect to the websocket
        :param url: URL to connect to
        :param app: Ref back to object that launched the WS
        :param token: Client token to to WS authentication
        """
        WebSocketClientFactory.__init__(self, f"ws://{url}", headers={
            "authorization": token
        })
        self.app = app
        self._protocol = None
