import requests
import PySimpleGUI
import classes

# Consts
version = "0.0.1"
server = "localhost:4000"
# Global Var
user = classes.BootStrap(server, version)
profile = None


def start_up():
    valid_token = user.validate_token()
    # TODO add code to pop up login if false
    profile = user.get_profile()
    # TODO display profile on window


if __name__ == '__main__':
    start_up()