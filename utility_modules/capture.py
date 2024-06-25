from datetime import datetime

import mss
import numpy as np
import cv2
import utility_modules.move_ctype as cici
from time import sleep

def capture_mode(mode, region=None, name=None):
    with mss.mss() as sct:
        match mode:
            case 'map':
                region_window = (530, 360, 1340, 890)
                cici.press_key('m')
                sleep(0.15)
                screenshot = sct.grab(region_window)
                sleep(0.05)
                cici.press_key('m')
                screenshot_np = np.array(screenshot)
                screenshot_prepared = cv2.cvtColor(screenshot_np, cv2.COLOR_RGBA2RGB)
                return screenshot_prepared

            case 'radar':
                region_window = (1647, 2, 1914, 268)
                screenshot = sct.grab(region_window)
                screenshot_np = np.array(screenshot)
                screenshot_prepared = cv2.cvtColor(screenshot_np, cv2.COLOR_RGBA2RGB)
                return screenshot_prepared

            case 'infobox':
                region_window = (0, 440, 400, 640)
                screenshot = sct.grab(region_window)
                screenshot_np = np.array(screenshot)
                screenshot_prepared = cv2.cvtColor(screenshot_np, cv2.COLOR_RGBA2RGB)
                return screenshot_prepared

            case 'desired':
                screenshot = sct.grab(region)
                screenshot_np = np.array(screenshot)
                screenshot_prepared = cv2.cvtColor(screenshot_np, cv2.COLOR_RGBA2RGB)
                return screenshot_prepared

            case 'listed_auctions':
                #search / favourites window
                region_window = (212, 218, 804, 617)
                screenshot = sct.grab(region_window)
                screenshot_np = np.array(screenshot)
                screenshot_prepared = cv2.cvtColor(screenshot_np, cv2.COLOR_RGBA2RGB)
                return screenshot_prepared

            case 'fhd':
                screenshot = sct.shot(output=name)
                return screenshot

            case 'addon_coords':

                region_window = (835, 1050, 1050, 1051)

                screenshot = sct.grab(region_window)
                screenshot_np = np.array(screenshot)
                screenshot_prepared = cv2.cvtColor(screenshot_np, cv2.COLOR_RGBA2RGB)
                if sum(screenshot_prepared[0,-1]) != 384:
                    print(screenshot_prepared[0,-1])
                    return False


                return screenshot_prepared




def crop(image, mode, map_position=None):
    match mode:
        case ('rarrow'):
            h, w, _ = image.shape
            hc, hw = int(h / 2), int(w / 2)
            cropped_image = image[hc - 16:hc + 16, hw - 16:hw + 16]
            return cropped_image

        case('marrow'):
            cropped_image = image[map_position[1] - 16:map_position[1] + 16, map_position[0] - 16:map_position[0] + 16]

            return cropped_image
