# this script simply press a random key in a randomly selected time, no CV involved
import pyautogui
import random
import time
import logging

max_seconds = 60 * 10
random_keys = ['w', 'a', 's', 'd', 'space']

def main():
    while True:
        key = random_keys[random.randint(0, len(random_keys) - 1)]
        delay = random.randint(1, max_seconds)
        logging.info("infinite loop: key = " + key + ", delay = " + str(delay))
        pyautogui.keyDown(key)
        time.sleep(0.3)
        pyautogui.keyUp(key)
        time.sleep(delay)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()