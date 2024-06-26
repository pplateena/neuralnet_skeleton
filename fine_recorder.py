import cv2
import matplotlib as plt
from pyautogui import position
from time import sleep, time
from utility_modules.capture import capture_mode
from utility_modules.move_ctype import RMB_down, LMB_down

from pynput.mouse import Listener, Controller
from pynput import keyboard, mouse
from multiprocessing import Process

def scalar_mousepos(mx, my):
    # mx, my = position()
    scalar_mx, scalar_my = round(mx/1920, 4) ,round(my/1080, 4)
    return scalar_mx, scalar_my

def record_mouse(db_number):
    def on_click(x, y, button, pressed):

        if pressed == True:
            print(button, x, y)
            sct = capture_mode('desired', region =(0,0,1920,1080))
            timing = round(time(), 1)

            cv2.imwrite(f'dataset/M_{button}_{x}_{y}_{timing}.jpg', sct)

    print('starting M')

    with Listener(on_click=on_click) as mouse_listener:
        mouse_listener.join()
        print('ua')
def record_kb(db_number):
    looking_for = {'q','w','e','r','t'}
    def on_kbpress(key):
        mouse_controller = Controller()

        try:
            actual_key = format(key.char)
            if actual_key in looking_for:
                m_pos = mouse_controller.position
                x,y = m_pos[0], m_pos[1]
                sct = capture_mode('desired', region =(0,0,1920,1080))
                timing = round(time(), 1)
                cv2.imwrite(f'dataset/KB_{actual_key}_{x}_{y}_{timing}.jpg', sct)
                print('rap')



        except AttributeError:
            if str(key) == "Key.space":
                m_pos = mouse_controller.position
                x,y = m_pos[0], m_pos[1]
                sct = capture_mode('desired', region =(0,0,1920,1080))
                timing = round(time(), 1)
                cv2.imwrite(f'dataset/KB_space_{x}_{y}_{timing}.jpg', sct)
                print('rap')

            else:

                print('special key {0} pressed'.format(key))

    print('starting KB')
    with keyboard.Listener(on_press=on_kbpress) as listener:
        listener.join()
if __name__ == '__main__':
    db_number = 'b' #input("enter db dataset starting_number")
    mouse = Process(target=record_mouse, args=db_number,)
    keyboard = Process(target=record_kb, args=db_number,)
    mouse.start()
    # keyboard.start()
    mouse.join()
    # keyboard.join()
    print('finita')