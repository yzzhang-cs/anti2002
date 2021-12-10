# for clicking/typing etc.
from numpy import short
import pyautogui as gui
# dependency
from PIL.Image import core as _imaging
# for handling arguments
import sys
# for random keys
import random
# for delays
import time
# for logging
import logging

image_waiting = './images/waiting.png'
image_2002 = './images/2002.png'
image_login_button = './images/login_button.png'
image_play_button = './images/play_button.png'
image_password_box = './images/password_box.png'
image_icon = './images/ffxiv_icon.png'
image_sprint = './images/sprint.png'
image_start = './images/game_start.png'
image_response = './images/response.png'
image_90002 = './images/90002.png'

random_keys = ['w', 'a', 's', 'd', 'space']
max_seconds = 60 * 10
small_delay = 1
delay = 5
n_tries = 5

def short_delay():
    time.sleep(small_delay)

def long_delay():
    time.sleep(delay)

# Find the game icon on Desktop and double click
# return:
#   True if success
def boot_game():
    logging.info('booting game')
    # double click icon
    icon_loc = None
    while not icon_loc:
        logging.info('looking for game icon')
        icon_loc = gui.locateCenterOnScreen(image_icon, confidence=0.9)
        short_delay()
    logging.info('game icon found, starting game')
    gui.doubleClick(icon_loc)
    return True

# Find the password box on the screen and enter password
# params:
#   username: currently useless. It is supposed to be entered into the login box
#   password: password to be entered
# return:
#   True if success
def login(username, password):
    logging.info('logging in')
    password_box = None
    while not password_box:
        logging.info('looking for password box')
        password_box = gui.locateCenterOnScreen(image_password_box, confidence=0.9)
        short_delay()
    logging.info('password box found, entering password')
    gui.leftClick(password_box)
    short_delay()
    gui.typewrite(password)

    login_button = None
    while not login_button:
        logging.info('looking for login button')
        login_button = gui.locateCenterOnScreen(image_login_button)
        short_delay()
    logging.info('login button found, click')
    gui.leftClick(login_button)

    play_button = None
    while not play_button:
        logging.info('looking for play button')
        play_button = gui.locateCenterOnScreen(image_play_button)
        short_delay()
    logging.info('play button found, click')
    gui.leftClick(play_button)

    return True

# Start the game by finding and hitting num0 on "GAME START"
# return:
#   True if success, False if failed(2002)
def start_game():
    start = None
    while not start:
        logging.info('looking for game start')
        start = gui.locateCenterOnScreen(image_start)
        short_delay()
    logging.info('game start button found, click')
    gui.moveTo(start)
    gui.press('num0')
    short_delay()
    gui.press('num0')
    response = None
    disconnected = None
    while not response and not disconnected:
        logging.info('looking for response')
        disconnected = gui.locateCenterOnScreen(image_2002)
        response = gui.locateCenterOnScreen(image_response, confidence=0.9)
        short_delay()
    if response:
        logging.info('response found, entering game')
        gui.press('num0')
        short_delay()
        gui.press('num0')
        return True
    if disconnected:
        logging.info('2002')
        gui.press('num0')
        short_delay()
        gui.press('num0')
        return False

# Wait in waitlist
# return:
#   True if already in the game, False if failed(2002)
def wait():
    disconnected = None
    sprint = None
    while not disconnected and not sprint:
        logging.info('in waitlist, waiting')
        disconnected = gui.locateCenterOnScreen(image_2002)
        sprint = gui.locateCenterOnScreen(image_sprint, grayscale=True, confidence=0.9)
        long_delay()
    if sprint:
        logging.info('in game')
        return True
    if disconnected:
        logging.info('2002')
        gui.press('num0')
        short_delay()
        gui.press('num0')
        return False

# Press a random key in randomly choosen time period, to prevent being kicked by the server.
# return:
#   False if 2002 or 90002
def hold():
    disconnected = None
    while not disconnected:
        logging.info('in game, holding')
        disconnected = gui.locateOnScreen(image_2002)
        if not disconnected:
            disconnected = gui.locateOnScreen(image_90002)
        key = random_keys[random.randint(0, len(random_keys) - 1)]
        wait_time = random.randint(0, max_seconds)
        gui.keyDown(key)
        time.sleep(0.3)
        gui.keyUp(key)
        print('holding... pressing key: ' + key + ' and wait ' + str(wait_time) + ' seconds')
        time.sleep(wait_time)
    logging.info('2002 or 90002')
    gui.press('num0')
    short_delay()
    gui.press('num0')
    return False



def main(username, password):
    logging.info('program started')
    for _ in range(n_tries):
        logging.info('trying to find out current status...')
        sprint = gui.locateCenterOnScreen(image_sprint)
        waiting = gui.locateCenterOnScreen(image_waiting)
        if sprint:
            logging.info('sprint icon found, in game')
            hold()
        elif waiting:
            logging.info('waiting message found, in waitlist')
            wait()
        short_delay()
    while True:
        boot_game()
        login(username, password)
        if not start_game():
            continue
        if not wait():
            continue
        if not hold():
            gui.hotkey('win', 'd')

        
    


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print('usage: \n\tpython rewaitlist.py [username] [password] \nor:\tpython rewaitlist.py [password]')
    else:
        if len(sys.argv) == 2:
            main(None, sys.argv[1])
        else:
            main(sys.argv[1], sys.argv[2])
#    main(sys.argv[1], sys.argv[2])