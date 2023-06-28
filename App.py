import sys
import cv2
import numpy as np
import keyboard
import win32api, win32con
import time
import threading
from time import process_time
import mss

class Detector:
    ZONE_X = 700
    ZONE_Y = 250
    ZONE_WIDTH = 550
    ZONE_HEIGHT = 650
    CHECK_REGION_SIZE = 2
    SPEED_OFFSET = 120
    LINES = [30, 160, 300, 430]

    def __init__(self):
        self.__sct = mss.mss(with_cursor = False)
        self.__kernel = np.zeros((self.CHECK_REGION_SIZE, self.CHECK_REGION_SIZE))
        self.__monitor = {"top": self.ZONE_Y, "left": self.ZONE_X, "width": self.ZONE_WIDTH, "height": self.ZONE_HEIGHT}
        self.__pointer_offset = (self.ZONE_X, self.ZONE_Y + self.SPEED_OFFSET)
        self.__check_positions = list([(x, y) for y in range(self.ZONE_HEIGHT - self.CHECK_REGION_SIZE, 0, -30) for x in self.LINES])

    def __get_black_pos(self, binary):
        region_size = self.CHECK_REGION_SIZE
        for x, y in self.__check_positions:
            if np.array_equal(binary[y:y + region_size, x:x + region_size], self.__kernel):
                return (x + region_size // 2, y + region_size // 2)
        return None
    
    def __detect_black_tile(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
        return self.__get_black_pos(binary)
    
    def get_screenshot(self):
        screenshot = self.__sct.grab(self.__monitor)
        image = np.array(screenshot)
        return image
    
    def get_tile_pos(self):
        screenshot = self.get_screenshot()
        zone_position = self.__detect_black_tile(screenshot)
        if not zone_position:
            return None
        
        cursor_x = np.add(self.__pointer_offset[0], zone_position[0])
        cursor_y = np.add(self.__pointer_offset[1], zone_position[1])

        return (cursor_x, cursor_y)

def wait_until_start():
    while True:
        time.sleep(0.05)
        if keyboard.is_pressed('q'):
            time.sleep(0.1)
            break

DEBUG = False
RECORD = False

def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
    
def draw_detector_debug(detector):
    wait_until_start()
    screenshot = detector.get_screenshot()
    for line in detector.LINES:
        screenshot = cv2.circle(screenshot, (line,0), radius=10, color=(255, 0, 0), thickness=-1)
    cv2.imshow('image', screenshot)
    cv2.waitKey(0)
    time.sleep(0.5)

def main():
    detector = Detector()

    video = None
    if RECORD:
        video=cv2.VideoWriter('video.avi', cv2.VideoWriter_fourcc(*'DIVX'), 10, (detector.ZONE_WIDTH, detector.ZONE_HEIGHT))
    if DEBUG:
        draw_detector_debug(detector)
    wait_until_start()
    print('---DETECTING STARTED---\a')

    exit_flag = False
    while not exit_flag:
        start_time = process_time()

        ###TILE DETECTION###
        d_start_time = process_time()
        pos = detector.get_tile_pos()
        d_end_time = process_time()
        ####################

        if RECORD and pos:
            screenshot = detector.get_screenshot()
            screenshot = cv2.circle(screenshot, (pos[0] - detector.ZONE_X, pos[1] - detector.ZONE_Y - detector.SPEED_OFFSET), radius=10, color=(0, 0, 255), thickness=-1)
            screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGBA2RGB)
            video.write(screenshot)

        ###CLICKING###
        c_start_time = process_time()
        if pos:
            if DEBUG: print(f'click {pos}')
            click(pos[0], pos[1])
        c_end_time = process_time()                    
        ##############

        end_time = process_time()
        if DEBUG and (end_time - start_time) > 0:
            print(f'frame time: {1 / (end_time - start_time)}', (end_time - start_time), (d_end_time - d_start_time), (c_end_time - c_start_time))

        if keyboard.is_pressed('q'):
            exit_flag = True
    
    if video:
        video.release()

    print('---DETECTING ENDED---\a')

if __name__ == '__main__':
    main()