import cv2
import matplotlib as plt
from pyautogui import position
from time import sleep, time
from utility_modules.capture import capture_mode

def scalar_mousepos():
    mx, my = position()
    scalar_mx, scalar_my = round(mx/1920, 4) ,round(my/1080, 4)
    return scalar_mx, scalar_my


def analyzer(dicty_number):
    n = 0
    mouse_moves = []

    while True:
        if n == 0:
            capture_mode('fhd', name= f'dataset/{dicty_number}_1.png')
        cycle_start_time = time()

        moving_x, moving_y = scalar_mousepos()
        mouse_moves.append([(moving_x, moving_y), time()])
        cycle_time = time() - cycle_start_time
        if cycle_time < 1/20:
            sleep(1/20-cycle_time)

        n += 1
        if n == 20:
            break
        elif n == 10:
            capture_mode('fhd', name= f'dataset/{dicty_number}_2.png')

    middle = int(len(mouse_moves)/2)
    print(middle)
    middle_time = mouse_moves[middle][1]

    for entry_index in range(len(mouse_moves)):

        if entry_index == middle:
            mouse_moves[middle][1] = 0
        # elif entry_index < middle:
        #     mouse_moves[entry_index][1] = mouse_moves[entry_index][1] - middle_time
        else:
            mouse_moves[entry_index][1] = round(mouse_moves[entry_index][1] - middle_time, 3)
    print(mouse_moves)
    draw = False
    if draw: ## img drawing
        for entry_index in range(int(len(mouse_moves)/2)):
            start_point = (round(mouse_moves[entry_index][0][0]*1920), round(mouse_moves[entry_index][0][1]*1080))
            end_point= (round(mouse_moves[entry_index + 1][0][0]*1920), round(mouse_moves[entry_index + 1][0][1]*1080))
            color = (255, 255, 0)  # Green color
            thickness = 5
            tip_length = 0.1
            img = cv2.imread(f'dataset/{dicty_number}_1.png')
            # print(start_point, end_point)
            img = cv2.drawMarker(img, start_point, (0, 255, 255), thickness = 5)
            img = cv2.arrowedLine(img, start_point, end_point, color, thickness, tipLength=tip_length)
            cv2.imwrite(f'dataset/{dicty_number}_1.png', img)

if __name__ == '__main__':
    analer = 0
    while analer < 100:

        analyzer(analer)
        analer += 1