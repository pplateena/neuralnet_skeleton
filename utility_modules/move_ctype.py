import ctypes
from time import sleep
import random
from math import ceil

# Load the user32.dll library
user32 = ctypes.windll.user32

# Define mouse event constants
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_ABSOLUTE = 0x8000
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
SM_CXSCREEN = 0
SM_CYSCREEN = 1

# Get the screen width and height
screen_width = user32.GetSystemMetrics(SM_CXSCREEN)
screen_height = user32.GetSystemMetrics(SM_CYSCREEN)


# Define the MouseInput structure
class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]


# Define the Input structure
class Input(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = [("mi", MouseInput)]

    _anonymous_ = ("_input",)
    _fields_ = [("_type", ctypes.c_ulong), ("_input", _INPUT)]


# Define input event constants
INPUT_MOUSE = 0
INPUT_KEYBOARD = 1  # Add this line for keyboard input


def calculate_rotation_direction(player_angle, checkpoint_angle, delta_only=False):
    import math

    def generate_list(number):

        result_list = []
        if number < 0:
            while number <= -960:
                result_list.append(-960)
                number += 960
            if number != 0:
                result_list.append(number)
        else:
            while number >= 960:
                result_list.append(960)
                number -= 960
            if number > 0:
                result_list.append(number)
        return result_list

    delta = 0
    if abs(player_angle - checkpoint_angle) > 180:
        if checkpoint_angle > player_angle:
            delta = (checkpoint_angle - 360) - player_angle
        if player_angle > checkpoint_angle:
            delta = (360 - player_angle) + checkpoint_angle
    else:
        if player_angle > checkpoint_angle:
            delta = checkpoint_angle - player_angle
        if checkpoint_angle > player_angle:
            delta = checkpoint_angle - player_angle

    counter = 1

    delta = delta / 0.96875

    if delta_only:
        return delta

    moves_list = []
    if delta < 0:
        total_moves = delta / 120

        limit_rotation = 960

        axis = total_moves * limit_rotation

        moves_list = generate_list(axis)
        return moves_list


    else:

        total_moves = delta / 120
        limit_rotation = 960

        axis = total_moves * limit_rotation

        moves_list = generate_list(axis)

        return moves_list


def press_right_button():
    input_ = Input()
    input_._type = INPUT_MOUSE
    input_._input.mi.dwFlags = MOUSEEVENTF_RIGHTDOWN
    user32.SendInput(1, ctypes.byref(input_), ctypes.sizeof(input_))


def release_right_button():
    input_ = Input()
    input_._type = INPUT_MOUSE
    input_._input.mi.dwFlags = MOUSEEVENTF_RIGHTUP
    user32.SendInput(1, ctypes.byref(input_), ctypes.sizeof(input_))


# Define input event constants
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004


def press_left_button():
    input_ = Input()
    input_._type = INPUT_MOUSE
    input_._input.mi.dwFlags = MOUSEEVENTF_LEFTDOWN
    user32.SendInput(1, ctypes.byref(input_), ctypes.sizeof(input_))


def release_left_button():
    input_ = Input()
    input_._type = INPUT_MOUSE
    input_._input.mi.dwFlags = MOUSEEVENTF_LEFTUP
    user32.SendInput(1, ctypes.byref(input_), ctypes.sizeof(input_))


def move_mouse_steps(end_x, end_y):
    start_x = 960
    start_y = 540
    diff = end_x - 960

    coef = 1 - (1000 - abs(diff)) / 1000

    num_steps = ceil(2 + 10 * coef)

    step_duration = 0.03
    dx = (end_x - start_x) / num_steps
    dy = (end_y - start_y) / num_steps

    press_right_button()  # Press right mouse button
    sleep(0.03)

    for step in range(1, num_steps + 1):
        x = start_x + int(dx * step)
        y = start_y + int(dy * step)

        input_ = Input()
        input_._type = INPUT_MOUSE
        input_._input.mi.dx = int(x * 65536 / screen_width)
        input_._input.mi.dy = int(y * 65536 / screen_height)
        input_._input.mi.dwFlags = MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE

        user32.SendInput(1, ctypes.byref(input_), ctypes.sizeof(input_))

        sleep(step_duration)  # Random sleep time

    release_right_button()
    sleep(0.03)


def move_cursor_steps(end_x, end_y):
    from pyautogui import position
    current_position = position()
    start_x = current_position[0]
    start_y = current_position[1]

    num_steps = 5

    step_duration = 0.02
    dx = (end_x - start_x) / num_steps
    dy = (end_y - start_y) / num_steps
    sleep(0.03)
    for step in range(1, num_steps + 1):
        x = start_x + int(dx * step)
        y = start_y + int(dy * step)

        input_ = Input()
        input_._type = INPUT_MOUSE
        input_._input.mi.dx = int(x * 65536 / screen_width)
        input_._input.mi.dy = int(y * 65536 / screen_height)
        input_._input.mi.dwFlags = MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE

        user32.SendInput(1, ctypes.byref(input_), ctypes.sizeof(input_))

        sleep(step_duration)  # Random sleep time


# Define constants for keyboard keys
VK_CODES = {
    '1': 0x31, '2': 0x32, '3': 0x33, '4': 0x34, '5': 0x35,
    '6': 0x36, '7': 0x37, '8': 0x38, '9': 0x39, '0': 0x30,
    'a': 0x41, 'b': 0x42, 'c': 0x43, 'd': 0x44, 'e': 0x45, 'f': 0x46, 'g': 0x47,
    'h': 0x48, 'i': 0x49, 'j': 0x4A, 'k': 0x4B, 'l': 0x4C, 'm': 0x4D, 'n': 0x4E,
    'o': 0x4F, 'p': 0x50, 'q': 0x51, 'r': 0x52, 's': 0x53, 't': 0x54, 'u': 0x55,
    'v': 0x56, 'w': 0x57, 'x': 0x58, 'y': 0x59, 'z': 0x5A,
    '!': 0x31, '@': 0x32, '#': 0x33, '$': 0x34, '%': 0x35,
    '^': 0x36, '&': 0x37, '*': 0x38, '(': 0x39, ')': 0x30,
    '-': 0xBD, '_': 0xBD, '=': 0xBB, '+': 0xBB,
    '[': 0xDB, '{': 0xDB, ']': 0xDD, '}': 0xDD,
    '\\': 0xDC, '|': 0xDC, ';': 0xBA, ':': 0xBA,
    "'": 0xDE, '"': 0xDE, ',': 0xBC, '<': 0xBC,
    '.': 0xBE, '>': 0xBE, '/': 0xBF, '?': 0xBF,
    'enter': 0x0D, 'space': 0x20, 'esc': 0x1B, 'shift': 0x10, 'tab': 0x09,
    'win': 0x5C, 'ctrl': 0x11,
    'arrow_up': 0x26, 'arrow_down': 0x28, 'arrow_left': 0x25, 'arrow_right': 0x27,

}


# Function to simulate a single key press
def press_key(key, hold=0):
    if key in VK_CODES:
        vk_code = VK_CODES[key]
        user32.keybd_event(vk_code, 0, 0, 0)  # Key down
        sleep(hold)
        user32.keybd_event(vk_code, 0, 0x0002, 0)  # Key up


def keybd_down(key):
    if key in VK_CODES:
        vk_code = VK_CODES[key]
        user32.keybd_event(vk_code, 0, 0, 0)  # Key down


def keybd_up(key):
    if key in VK_CODES:
        vk_code = VK_CODES[key]
        user32.keybd_event(vk_code, 0, 0x0002, 0)

    # Function to type a string


def type_string(text):
    typing_interval = random.uniform(0.07, 0.3)

    for char in text:
        if char is " ":
            press_key('space')

        if char.isupper() or char == '@':

            keybd_down('shift')

            press_key(char.lower(), typing_interval)
            keybd_up('shift')  # Release Shift
        else:
            press_key(char, typing_interval)


def gas(distance, speed):
    press_key('w', distance / speed)



def LMB_down():
    VK_LBUTTON = 0x01

    user32 = ctypes.windll.user32
    short = ctypes.c_short
    GetAsyncKeyState = user32.GetAsyncKeyState
    GetAsyncKeyState.argtypes = [short]
    GetAsyncKeyState.restype = short
    key_state = GetAsyncKeyState(VK_LBUTTON)
    return key_state & 0x8000 != 0  # Check if least significant bit is set (indicates pressed)

def RMB_down():
    VK_RBUTTON = 0x02

    user32 = ctypes.windll.user32
    short = ctypes.c_short
    GetAsyncKeyState = user32.GetAsyncKeyState
    GetAsyncKeyState.argtypes = [short]
    GetAsyncKeyState.restype = short
    key_state = GetAsyncKeyState(VK_RBUTTON)
    return key_state & 0x8000 != 0  # Check if least significant bit is set (indicates pressed)