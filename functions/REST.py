"""
Holds all of the functions for the rest API that aren't contained in a class
"""
import requests
import json
from typing import Optional


def create_account(basrURL: str, email: str, password: str, username: str, firstname: str, lastname: str):
    response = requests.post(f"http://{basrURL}/createAccount", data={
        "email": email,
        "password": password,
        "username": username,
        "firstName": firstname,
        "lastName": lastname
    })
    if response.status_code != 200:
        return False, response.json()['message']
    elif response.status_code == 200:
        return True
