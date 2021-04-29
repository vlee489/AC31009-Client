"""
Contains the window defs for login GUI
"""
import PySimpleGUI as sg


def login_window(message: str) -> sg.Window:
    """
    Get login window layout
    :param message: Message to display
    :return: window
    """
    layout = [
        [sg.Text(message)],
        [sg.Text('Email: '), sg.InputText()],
        [sg.Text('Password: '), sg.InputText(password_char="*")],
        [sg.Button('Login'), sg.Button('Create Account')]
    ]
    return sg.Window("login", layout)


def login_success() -> sg.Window:
    """
    get Login success window
    :return: window
    """
    layout = [
        [sg.Text('Login Successful!')],
    ]
    return sg.Window("Login Successful", layout, auto_close_duration=2, auto_close=True)


def create_account_window(message: str) -> sg.Window:
    """
    Get create account window
    :param message: Message to display
    :return: window
    """
    layout = [
        [sg.Text(message)],
        [sg.Text('Email: '), sg.InputText()],
        [sg.Text('Password: '), sg.InputText(password_char="*")],
        [sg.Text('Username: '), sg.InputText()],
        [sg.Text('First Name: '), sg.InputText()],
        [sg.Text('Last Name: '), sg.InputText()],

        [sg.Button('Create Account')]
    ]
    return sg.Window("login", layout)


def create_successful_window() -> sg.Window:
    """
    Get create account success window
    :return: window
    """
    layout = [
        [sg.Text('Create Account Successful!')],
    ]
    return sg.Window("Create Account Successful", layout, auto_close_duration=2, auto_close=True)


def server_down_window():
    """
    get server down dialog
    :return:
    """
    layout = [
        [sg.Text("Server is currently unavailable!")],
        [sg.Text("Please try again later when server are available!")],
        [sg.Button('Exit')]
    ]
    return sg.Window("Error", layout)

