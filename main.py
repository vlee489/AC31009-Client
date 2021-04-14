import requests
import PySimpleGUI as sg
import classes
import time
import functions
import logging

# Consts
version = "0.0.1"
server = "localhost:4000"
# Global Var
user = classes.BootStrap(server, version)
profile = None


def start_up():
    logging.info("Validating User Token")
    valid_token = user.validate_token()
    if not valid_token:
        logging.info("Invalid/no-existent token, starting login procedure")
        login_gui()
    profile = user.get_profile()
    # TODO display profile on window


def login_gui():
    """
    Runs Login window and procedures
    :return:
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
                                                                 create_values[2], create_values[3], create_values[4])
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
