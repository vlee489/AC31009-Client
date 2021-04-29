import PySimpleGUI as sg
import classes
import functions
from twisted.internet import reactor
from twisted.internet.task import Cooperator
import sys
import os
import requests

# Consts
version = "0.0.1"  # Game Version for gameData matching
server = "node1.vlee.me.uk:4000"  # Location of server with port
port = 4000  # Port server is running on Used for Twisted Reactor
secure = True
# Global Var
user = None

# To get pyInstaller working
# https://stackoverflow.com/questions/28033003/pyinstaller-with-pygame
if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)


def start_up():
    global user
    print("Checking if server is up")
    # Checks if server is up
    if secure:
        protocol = "https"
    else:
        protocol = 'http'
    try:
        requests.get(f"{protocol}://{server}/gameData")
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        # if we get a time out means server is down, so we create a popup
        print("Server is down!")
        while True:
            window = functions.server_down_window()
            event, values = window.read()  # read values
            if event == "Exit" or event == sg.WIN_CLOSED:
                exit(10)
    user = classes.BootStrap(server, version, port, secure)  # user bootstrap with user details
    print("Validating User Token")
    valid_token = user.validate_token()
    if not valid_token:
        print("Invalid/no-existent token, starting login procedure")
        login_gui()


def login_gui():
    """
    Runs Login window and procedures
    :return: None
    """
    window = functions.login_window('Please Login')  # create login window
    while True:
        event, values = window.read()  # read values
        if event == "Login":
            # Attempt to login
            response = user.login(values[0], values[1])
            if response:  # If true show window and close
                window = functions.login_success()
            else:
                window = functions.login_window('Login Unsuccessful')
        elif event == "Create Account":
            # Open window to create account
            create_account_window = functions.create_account_window("Create Account")
            while True:
                create_event, create_values = create_account_window.read()
                if create_event == "Create Account":
                    # Attempt to create new account
                    response, message = functions.create_account(server, create_values[0], create_values[1],
                                                                 create_values[2], create_values[3], create_values[4],
                                                                 secure)
                    if response:
                        # If we create the account, send back to login window
                        create_account_window.close()
                        window = functions.login_window("Account Created, Please login!")
                        break
                    else:
                        # If there's an error open the create window again with the error
                        create_account_window = functions.create_account_window(f"Unable to create Account: {message}")
                elif create_event == sg.WIN_CLOSED:
                    break
        elif event == sg.WIN_CLOSED:
            break


if __name__ == '__main__':
    start_up()
    app = classes.App(user)
    coop = Cooperator()
    coop.coiterate(app.main())
    reactor.run()  # Start the Twisted reactor.
