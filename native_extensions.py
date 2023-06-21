import ctypes
import numpy as np
import cv2
import time
LIB_PATH = './CppExtensions/x64/CppExtensions.dll'
lib = ctypes.CDLL(LIB_PATH)

take_screenshot = lib.take_screenshot
take_screenshot.argtypes = [ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int]
take_screenshot.restype = ctypes.POINTER(ctypes.c_ubyte)
freep =lib.freep
freep.argtypes = [ctypes.POINTER(ctypes.c_ubyte)]

# used to record the time when we processed last frame
prev_frame_time = 0
  
# used to record the time at which we processed current frame
new_frame_time = 0
frame = 0
while True:
    p = take_screenshot(0, 0, 500, 500)
    n = np.ctypeslib.as_array(p, (500,500,4))
    n = cv2.flip(n, 0)

    new_frame_time = time.time()
    fps = 1/(new_frame_time-prev_frame_time)
    prev_frame_time = new_frame_time
    fps = int(fps)
    
    frame += 1
    if frame > 10:
        print(fps)
        frame = 0

    cv2.imshow("image", n)
    del n
    freep(p)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
