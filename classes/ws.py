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
        print('WebSocket connection open.')
        self.factory._protocol = self

    def onMessage(self, payload, is_binary):
        """
        Configures what happens when a new message comes via WS
        :param payload:
        :param is_binary:
        :return:
        """
        if is_binary:
            msg = 'Binary message received: {0} bytes'.format(len(payload))
        else:
            data = json.loads(payload.decode('utf8'))
            if isinstance(self.factory.app.game, Game):
                self.factory.app.game.messages.append(data)

    def onClose(self, was_clean, code, reason):
        """
        Runs on WS connection close
        :param was_clean:
        :param code:
        :param reason:
        :return:
        """
        print('WebSocket connection closed: {0}'.format(reason))
        self.factory._protocol = None


class URPGClientFactory(WebSocketClientFactory):
    protocol = URPGClientProtocol

    def __init__(self, url: str, app, token: str):
        WebSocketClientFactory.__init__(self, f"ws://{url}", headers={
            "authorization": token
        })
        self.app = app
        self._protocol = None
