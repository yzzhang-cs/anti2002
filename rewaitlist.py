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

random_keys = ['w', 'a', 's', 'd', 'space']
max_seconds = 60
small_delay = 1
delay = 5
n_tries = 5

def short_delay():
    time.sleep(small_delay)

def long_delay():
    time.sleep(delay)


def boot_game():
    logging.info('booting game')
    # double click icon
    icon_loc = None
    while not icon_loc:
        logging.info('looking for game icon')
        icon_loc = gui.locateCenterOnScreen(image_icon)
        short_delay()
    logging.info('game icon found, starting game')
    gui.doubleClick(icon_loc)
    return True

def login(username, password):
    logging.info('logging in')
    password_box = None
    while not password_box:
        logging.info('looking for password box')
        password_box = gui.locateCenterOnScreen(image_password_box)
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
        response = gui.locateCenterOnScreen(image_response)
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

def wait():
    disconnected = None
    sprint = None
    while not disconnected and not sprint:
        logging.info('in waitlist, waiting')
        disconnected = gui.locateCenterOnScreen(image_2002)
        sprint = gui.locateCenterOnScreen(image_sprint)
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

def hold():
    disconnected = None
    while not disconnected:
        logging.info('in game, holding')
        disconnected = gui.locateOnScreen(image_2002)
        key = random_keys[random.randint(0, len(random_keys) - 1)]
        wait_time = random.randint(0, max_seconds)
        gui.press(key)
        print('holding... pressing key: ' + key + ' and wait ' + str(wait_time) + ' seconds')
        time.sleep(wait_time)
    logging.info('2002')
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
        hold()

        
    


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