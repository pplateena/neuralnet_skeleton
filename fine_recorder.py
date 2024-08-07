import cv2
import matplotlib as plt
from pyautogui import position
from time import sleep, time
from utility_modules.capture import capture_mode
from utility_modules.move_ctype import RMB_down, LMB_down

from pynput.mouse import Listener, Controller
from pynput import keyboard, mouse
from multiprocessing import Process
import playsound
photo_sound ='dataset/LootCoinSmall.mp3'

def record_mouse(saved_folder):
    def on_click(x, y, button, pressed):

        if pressed == True:
            button = str(button).split(".")[1]
            sct = capture_mode('desired', region =(0,0,1920,1080))
            timing = round(time(), 1)
            print(button, x, y)

            if saved_folder == "augmented_data":

                if button == "left":
                    cv2.imwrite(f'augmented_data/explore_img/M_{button}_{x}_{y}_{timing}.jpg', sct)
                else:
                    cv2.imwrite(f'augmented_data/attack_img/M_{button}_{x}_{y}_{timing}.jpg', sct)

            if saved_folder == "classification_data":
                cv2.imwrite(f'dataset/M_{button}_{x}_{y}_{timing}.jpg', sct)
            # playsound.playsound(photo_sound, block=False)

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

def record_special(saving_folder):
    print("special started")
    def on_kbpress(key):
        try:
            actual_key = format(key.char)
            print(actual_key)
            if actual_key == 'a':
                sct = capture_mode('desired', region=(0, 0, 1920, 1080))
                saved_image = cv2.resize(sct, (640, 360))
                timing = round(time(), 1)
                cv2.imwrite(f'{saving_folder}/attack_img/KB_{actual_key}_{timing}.jpg', saved_image)
            elif actual_key == 'q':
                sct = capture_mode('desired', region=(0, 0, 1920, 1080))
                saved_image = cv2.resize(sct, (640, 360))
                timing = round(time(), 1)
                cv2.imwrite(f'{saving_folder}/explore_img/KB_{actual_key}_{timing}.jpg', saved_image)
            else:
                print('{0} pressed'.format(key))

        except AttributeError:
            print('special key {0} pressed'.format(key))

    with keyboard.Listener(on_press=on_kbpress) as listener:
        listener.join()

def timer_record(saving_folder):
    print('timer_started')
    key = cv2.waitKey(1) & 0xFF

    while key != ord('x'):
        key = cv2.waitKey(1) & 0xFF
        sct = capture_mode('desired', region=(0, 0, 1920, 1080))
        saved_image = cv2.resize(sct, (640, 360))
        timing = round(time(), 1)
        cv2.imwrite(f'{saving_folder}/KB_{timing}.jpg', saved_image)
        print('saved file')
        sleep(4)

if __name__ == '__main__':
    saving_folder = 'augmented_data'

    if saving_folder == 'default_classification':
        # mouse = Process(target=record_mouse(),)
        keyboard = Process(target=record_special(),)
        # mouse.start()
        keyboard.start()
        # mouse.join()
        keyboard.join()
        print('finita')

    if saving_folder == 'augmented_data':
        mouse = Process(target=record_mouse, args=(saving_folder,))
        keyboard = Process(target=record_special, args=(saving_folder,))
        timer = Process(target=timer_record, args=(saving_folder,))

        timer.start()
        mouse.start()

        # keyboard.start()
        # timer.join()
        # keyboard.join()
