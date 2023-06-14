import sys
import cv2
import numpy as np
import keyboard
import pyautogui
import time
import threading
from time import process_time
import mss

class Detector:
    ZONE_X = 550
    ZONE_Y = 300
    ZONE_WIDTH = 700
    ZONE_HEIGHT = 600
    CHECK_REGION_SIZE = 70
    SPEED_OFFSET = 100

    __sct = None
    __kernel = None

    def __init__(self):
        self.__sct = mss.mss(with_cursor = False)
        self.__kernel = np.zeros((self.CHECK_REGION_SIZE, self.CHECK_REGION_SIZE))

    def __get_black_pos(self, binary):
        count = 0
        for y in range(self.ZONE_HEIGHT - self.CHECK_REGION_SIZE, 0, -30):
            for x in range(0, self.ZONE_WIDTH - self.CHECK_REGION_SIZE, 30):
                count += 1
                if (binary[y:y + self.CHECK_REGION_SIZE, x:x + self.CHECK_REGION_SIZE] \
                    == self.__kernel).all():
                    return (x + self.CHECK_REGION_SIZE // 2, y + self.CHECK_REGION_SIZE // 2)
        return None
    
    def __detect_black_tile(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)
        return self.__get_black_pos(binary)
    
    def __get_screenshot(self):
        screenshot = self.__sct.grab(self.__sct.monitors[1])
        image = np.array(screenshot)
        zone_image = image[self.ZONE_Y:self.ZONE_Y + self.ZONE_HEIGHT,
                           self.ZONE_X:self.ZONE_X + self.ZONE_WIDTH]
        return zone_image
    
    def get_tile_pos(self):
        screenshot = self.__get_screenshot()
        zone_position = self.__detect_black_tile(screenshot)
        if not zone_position:
            return None
        
        cursor_x = self.ZONE_X + zone_position[0]
        cursor_y = self.ZONE_Y + zone_position[1] + self.SPEED_OFFSET

        return (cursor_x, cursor_y)

def wait_until_start():
    while True:
        time.sleep(0.05)
        if keyboard.is_pressed('q'):
            time.sleep(0.1)
            break

DEBUG = False

def main():
    print('---DETECTING STARTED---\a')
    detector = Detector()

    exit_flag = False
    while not exit_flag:
        start_time = process_time()

        ###TILE DETECTION###
        d_start_time = process_time()
        pos = detector.get_tile_pos()
        d_end_time = process_time()
        ####################

        ###CLICKING###
        c_start_time = process_time()
        if pos:
            if DEBUG: print(f'click {pos}')
            pyautogui.click(pos[0], pos[1], _pause=False)
        c_end_time = process_time()                    
        ##############

        end_time = process_time()
        if DEBUG and (end_time - start_time) > 0:
            print(f'frame time: {1 / (end_time - start_time)}', (end_time - start_time), (d_end_time - d_start_time), (c_end_time - c_start_time))

        if keyboard.is_pressed('q'):
            exit_flag = True

    print('---DETECTING ENDED---\a')

if __name__ == '__main__':
    wait_until_start()
    main()
