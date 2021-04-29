"""
Holds all of the functions for the rest API that aren't contained in a class
"""
import requests


def create_account(base_url: str, email: str, password: str, username: str,
                   firstname: str, lastname: str, secure: bool):
    """
    Create an account with the server
    :param base_url: base URL of server
    :param email: email
    :param password: password
    :param username: username
    :param firstname: firstname
    :param lastname: lastname
    :param secure: If the server used SSL
    :return: If the account was successfully made or not
    """
    if secure:
        protocol = "https"
    else:
        protocol = "http"
    response = requests.post(f"{protocol}://{base_url}/createAccount", data={
        "email": email,
        "password": password,
        "username": username,
        "firstName": firstname,
        "lastName": lastname
    })
    if response.status_code != 200:
        return False, response.json()['message']
    elif response.status_code == 200:
        return True, None
