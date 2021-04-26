# AC31009-Client
Client for the AC31009 Game Module

## Requirements

- [Python 3.9](https://www.python.org/)
- pip (*typically installed with Python*)
- AC31009-Server hosted somewhere

## Install & Launch

*It's recommended you use Python's Virtual Environment, as installing packages via pip on Python 3.9+ requires admin
privileges when not using venv, if you use something like [Pycharm](https://www.jetbrains.com/pycharm/) it can set up venv for you during
project setup.*

0. Setup venv, instruction [here](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
1. `cd` into the root directory
2. Install the requirements with `pip install -r requirements.txt`
3. If you need to, edit `main.py` file with the url/ip and port the server is running on. This is located at the
   top of the file on lines 12 and 13.
4. Launch the client/game with `python main.py`

## Building Executable

You can use pyInstalled to create an executable for the game. To do this you can run `pyinstaller main.spec` from the 
command line linked to venv.

## Credits

### Sprites
The Sprites used are the follow. These are under their agreements listed on their Itch.io pages for these assets

- [Hero Knight by luizmelo](https://luizmelo.itch.io/hero-knight) Licenced under CC0
- [Wizard Pack by luizmelo](https://luizmelo.itch.io/wizard-pack) Licenced under CC0
- [Spirit Boxer from Sci-fi Character Pack 1 by https://penusbmic.itch.io/characterpack1](https://penusbmic.itch.io/characterpack1)
  
### Font
Fonts used

- [Montserrat by Julieta Ulanovsky, Sol Matas, Juan Pablo del Peral, Jacques Le Bailly](https://fonts.google.com/specimen/Montserrat)
, This font is licenced under the Open Font Licence.
  
## Packages

This project used a number of packages for different functions, and can be found on PyPi

- `Pygame`: Game engine, displays stuff using SDL2
- `requests`: HTTP/S requests
- `pysimplegui`: Used for login UI
- `autobahn` & `twisted`: Handles Websockets connection and concurrent operation alongside PyGame
- `ujson`: for autobahn for more efficient json parsing
- `wsaccel`: Websocket accelerator
- `pyinstaller`: Creates executable file