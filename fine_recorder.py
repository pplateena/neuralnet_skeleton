import cv2
import matplotlib as plt
from pyautogui import position
from time import sleep, time
from utility_modules.capture import capture_mode
from utility_modules.move_ctype import RMB_down, LMB_down

from pynput.mouse import Listener

def scalar_mousepos():
    mx, my = position()
    scalar_mx, scalar_my = round(mx/1920, 4) ,round(my/1080, 4)
    return scalar_mx, scalar_my
def on_click(x, y, button, pressed):
    if pressed:
      print(pressed, button, x,y)

def on_move(x, y):
    print('Pointer moved to {0}'.format(
        (x, y)))


def record_sequence():

    with Listener(on_click=on_click, on_move=on_move,) as listener:
        listener.join()  # Set listener timeout to 0.25 seconds

record_sequence()

# from pynput import keyboard
#
# def on_press(key):
#     try:
#         print('alphanumeric key {0} pressed'.format(
#             key.char))
#     except AttributeError:
#         print('special key {0} pressed'.format(
#             key))
#
# def on_release(key):
#     print('{0} released'.format(
#         key))
#     if key == keyboard.Key.esc:
#         # Stop listener
#         return False
#
# # Collect events until released
# with keyboard.Listener(
#         on_press=on_press,
#         on_release=on_release) as listener:
#     listener.join()
#
# # ...or, in a non-blocking fashion:
# listener = keyboard.Listener(
#     on_press=on_press,
#     on_release=on_release)
# listener.start()