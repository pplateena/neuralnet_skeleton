from ultralytics import YOLO
from pyautogui import press 
import keyboard
import time

from capture import capture_mode

def coords():
    model_LOCATION = YOLO('C:\\Users\\plat_move\\desktop\\10wow_reboot\\instruments\\LOCATION_FHD_NORESIZE_3.pt')
    model_LOCATION.to('cuda')

    print('loaded')
    

    while True:
        if keyboard.is_pressed('q'):
            MAP = capture_mode('map')
            results_LOCATION = model_LOCATION.predict(MAP)

            boxes = results_LOCATION[0].boxes

            if boxes:
                box = boxes.xyxy[0].tolist()
                location = [round((box[0]+box[2])/2),round((box[1]+box[3])/2)]
                print(location)

        time.sleep(0.01)
        
        if keyboard.is_pressed('z'):
            break

coords()



