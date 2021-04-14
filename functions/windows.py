import PySimpleGUI as sg


def login_window(message: str):
    layout = [
        [sg.Text(message)],
        [sg.Text('Email: '), sg.InputText()],
        [sg.Text('Password: '), sg.InputText(password_char="*")],
        [sg.Button('Login'), sg.Button('Create Account')]
    ]
    return sg.Window("login", layout)


def login_success():
    layout = [
        [sg.Text('Login Successful!')],
    ]
    return sg.Window("Login Successful", layout, auto_close_duration=2, auto_close=True)


def create_account_window(message: str):
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


def create_successful_window():
    layout = [
        [sg.Text('Create Account Successful!')],
    ]
    return sg.Window("Create Account Successful", layout, auto_close_duration=2, auto_close=True)
