import sys
import cv2
import numpy as np
import keyboard
import pyautogui
import time
import threading
from time import process_time
from mss import mss


sct = mss(with_cursor = False)

ZONE_X = 550
ZONE_Y = 170
ZONE_WIDTH = 700
ZONE_HEIGHT = 700
MAX_ZONE_SQUARE = 150*200
mon = {'top': ZONE_Y, 'left': ZONE_X, 'width': ZONE_WIDTH, 'height': ZONE_HEIGHT}

def detect_black_tile(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5,5), 0)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)
    binary_inverse = cv2.bitwise_not(binary)
    contours, _ = cv2.findContours(binary_inverse, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        return True, contours[0]
    else:
        return False, None

def is_cursor_on_black(screenshot, x, y):
    pixel = screenshot[y, x]
    print(pixel)
    return (pixel == [0, 0, 0, 255]).all()

def tile_detector():
    while True:
        time.sleep(0.05)
        if keyboard.is_pressed('q'):
            print('\a')
            break



    while not exit_flag.is_set():
        
        start_time = process_time()

        d_start_time = process_time()
        screenshot = sct.grab(sct.monitors[1])
        image = np.array(screenshot)
        zone_image = image[ZONE_Y:ZONE_Y + ZONE_HEIGHT, ZONE_X:ZONE_X + ZONE_WIDTH]

        is_black_tile, contour = detect_black_tile(zone_image)
        d_end_time = process_time()

        c_start_time = process_time()
        if is_black_tile:
            x, y, w, h = cv2.boundingRect(contour)
            if w*h <= MAX_ZONE_SQUARE:
                cX = x + w // 2
                cY = y + h // 2
                cursor_x = ZONE_X + cX
                cursor_y = ZONE_Y + cY + 100

                if is_cursor_on_black(image, cursor_x, cursor_y):
                    pyautogui.click(cursor_x, cursor_y, _pause=False)
        c_end_time = process_time()                    

        end_time = process_time()
        if (end_time - start_time) > 0:
            print(f'frame time: {1 / (end_time - start_time)}', (end_time - start_time), (d_end_time - d_start_time), (c_end_time - c_start_time))

        if keyboard.is_pressed('q'):
            exit_flag.set()
            print('\a')
            print('exit')

exit_flag = threading.Event()
exit_flag.clear()
#try:
#    thread = threading.Thread(target=tile_detector)
#    thread.start()
#    while thread.is_alive(): 
#        thread.join(1)
#except (KeyboardInterrupt, SystemExit):
#    print('\n! Received keyboard interrupt, quitting threads.\n')
#finally:
tile_detector()
exit_flag.set()
sys.exit()