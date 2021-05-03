# AC31009-Client
Client for the AC31009 Game Module

## Requirements

- [Python 3.9](https://www.python.org/)
- pip (*typically installed with Python*)
- AC31009-Server hosted somewhere

## Precompiled Executables 

You can download pre-built versions of the game from [Github Releases Here](https://github.com/vlee489/AC31009-Client/releases)

## Install & Launch

*It's recommended you use Python's Virtual Environment, as installing packages via pip on Python 3.9+ requires admin
privileges when not using venv, if you use something like [Pycharm](https://www.jetbrains.com/pycharm/) it can set 
up venv for you during project setup without you needing to do step 0.*

0. Setup venv, instruction [here](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
1. `cd` into the root directory
2. Install the requirements with `pip install -r requirements.txt`
3. If you need to, edit `main.py` file with the url/ip and port the server is running on. This is located at the
   top of the file on lines 12, 13 and 14
4. Launch the client/game with `python main.py`

## Building Executable

You can use pyInstalled to create an executable for the game. 

1. Edit `main.spec` line 11 so that the path stated where the folder is located on your system.
```python
pathex=['B:\\Git\\Univeristy\\Year 3\\AC31009-Client'],
```
2. Run `pyinstaller main.spec` from the command line linked to Python venv.

## Credits

### Sprites
The Sprites used are the follow. These are under their agreements listed on their Itch.io pages for these assets

- [Hero Knight by luizmelo](https://luizmelo.itch.io/hero-knight) Licenced under CC0
- [Wizard Pack by luizmelo](https://luizmelo.itch.io/wizard-pack) Licenced under CC0
- [Spirit Boxer from Sci-fi Character Pack 1 by penusbmic](https://penusbmic.itch.io/characterpack1)

## Background
Backgrounds used are from:

- [Free Pixel-art background, desert (Day/Night) by blank-can~~~~vas](https://blank-canvas.itch.io/parallax-pixel-art-background-desert)
  
### Font
Fonts used:

- [Montserrat by Julieta Ulanovsky, Sol Matas, Juan Pablo del Peral, Jacques Le Bailly](https://fonts.google.com/specimen/Montserrat)
, This font is licenced under the Open Font Licence.
  
### Icons

- [Back](https://fontawesome.com/icons/arrow-circle-left?style=solid) Font Awesome *Creative Commons Attribution 4.0 International license*

### Sounds

- [MixKit](https://mixkit.co/): for sounds from MixKit used under their licence [here](https://mixkit.co/license/#sfxFree)
- [Sound FX Pack 1 by edwardcufaude](https://edwardcufaude.itch.io/soundfxpack1): for sounds not starting with mixkit used under their licence
  
## Packages

This project used a number of packages for different functions listed in the `requirements.txt` file, 
and can be found on PyPi for more info.
