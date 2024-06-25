from capture_fhd import screenshot_mode,crop
from time import sleep
import os
import cv2
from ultralytics import YOLO


#model_LOCATION = YOLO('C:\\piton\\git\\plateenum\\7ver_wow\\instruments\\LOCATION_FHD_NORESIZE_3.pt') 


def get_last_screenshot_number(folder_path):
    prefix = f"map_"
    screenshot_number = 0  # Initialize the screenshot number
    for filename in os.listdir(folder_path):
        if filename.startswith(prefix):
            try:
                number = int(filename[len(prefix):-4])  # Extract the number part
                screenshot_number = max(screenshot_number, number)
            except ValueError:
                pass  # Ignore filenames that don't match the format

    return screenshot_number

folder_map = "C:/piton/git/plateenum/7ver_wow/assets/location_map_fhd"
folder_marrow = "C:/piton/git/plateenum/7ver_wow/assets/arrow_map"
folder_marrow_small = "C:/piton/git/plateenum/7ver_wow/assets/arrow_map_small"
folder_radar = "C:/piton/git/plateenum/7ver_wow/assets/radar"
folder_rarrow = "C:/piton/git/plateenum/7ver_wow/assets/arrow_radar_small"

def nocondition_capture():
    save_map = False
    save_map_arrow = False
    save_radar = False
    save_radar_arrow = True
    n = 0
    while n < 100:
        #MAP = screenshot_mode('map')  # Provide folder_path as an argument

        

        if save_map:
            
            filename_map = f"map_{screenshot_number + 1:04d}.png"  # Increment the screenshot_number
            output_path_map = os.path.join(folder_map, filename_map)
            cv2.imwrite(output_path_map, MAP)
        
        if save_map_arrow:

            results_LOCATION = model_LOCATION.predict(MAP)
            boxes = results_LOCATION[0].boxes
                
            if boxes:
                box = boxes.xyxy[0].tolist()
                location = [round((box[0]+box[2])/2),round((box[1]+box[3])/2)]
                ARROW = crop(MAP, 'arrow_map', location)

                filename_marrow  = f"marrow _{screenshot_number + 1:04d}.png"  # Increment the screenshot_number

                output_path_marrow = os.path.join(folder_marrow_small, filename_marrow)

                cv2.imwrite(output_path_marrow, ARROW)

        RADAR = screenshot_mode('radar')
       
        if save_radar:
            filename_radar  = f"radar_{screenshot_number + 1:04d}.png"
            output_path_radar = os.path.join(folder_radar, filename_radar)
            cv2.imwrite(output_path_radar, RADAR)

        if save_radar_arrow:
            ARROW = crop(RADAR, 'arrow_radar', 0)

            filename_radar_arrow  = f"rarrow_{screenshot_number + 1:04d}.png"
            output_path_radar = os.path.join(folder_rarrow, filename_radar_arrow)
            cv2.imwrite(output_path_radar, ARROW)


        screenshot_number += 1
        n +=1 
        sleep(0.3)




def conditioned_capture():
    target_dataset = screenshot_mode('desired', (930,510,990,570))
    _, _ , target_data_R = target_dataset[10,10]
    print(target_data_R)

    save_radar = True
    save_radar_arrow = True
    n = 0
    screenshot_number = get_last_screenshot_number(folder_radar)

    
    while n < 200:

        if target_data_R ==255:

            RADAR = screenshot_mode('radar')
           
            if save_radar:
                
                filename_radar  = f"radar_{screenshot_number + 1:04d}.png"
                output_path_radar = os.path.join(folder_radar, filename_radar)

                cv2.imwrite(output_path_radar, RADAR)

            if save_radar_arrow:
                
                ARROW = crop(RADAR, 'arrow_radar', 0)

                filename_radar_arrow  = f"rarrow_{screenshot_number + 1:04d}.png"
                output_path_radar = os.path.join(folder_rarrow, filename_radar_arrow)
                cv2.imwrite(output_path_radar, ARROW)


            screenshot_number += 1
            n +=1 
            sleep(1)


def save_runner_data(MAP,ARROW):
    save_map = True
    save_map_arrow = True
    screenshot_number_map = get_last_screenshot_number(folder_map)
    n = 0
    while n < 100:
        #MAP = screenshot_mode('map')  # Provide folder_path as an argument

        

        if save_map:
            
            filename_map = f"map_{screenshot_number + 1:04d}.png"  # Increment the screenshot_number
            output_path_map = os.path.join(folder_map, filename_map)
            cv2.imwrite(output_path_map, MAP)
        
        if save_map_arrow:

            results_LOCATION = model_LOCATION.predict(MAP)
            boxes = results_LOCATION[0].boxes
                
            if boxes:
                box = boxes.xyxy[0].tolist()
                location = [round((box[0]+box[2])/2),round((box[1]+box[3])/2)]
                ARROW = crop(MAP, 'arrow_map', location)

                filename_marrow  = f"marrow _{screenshot_number + 1:04d}.png"  # Increment the screenshot_number

                output_path_marrow = os.path.join(folder_marrow_small, filename_marrow)

                cv2.imwrite(output_path_marrow, ARROW)

        RADAR = screenshot_mode('radar')
       
        if save_radar:
            filename_radar  = f"radar_{screenshot_number + 1:04d}.png"
            output_path_radar = os.path.join(folder_radar, filename_radar)
            cv2.imwrite(output_path_radar, RADAR)

        if save_radar_arrow:
            ARROW = crop(RADAR, 'arrow_radar', 0)

            filename_radar_arrow  = f"rarrow_{screenshot_number + 1:04d}.png"
            output_path_radar = os.path.join(folder_rarrow, filename_radar_arrow)
            cv2.imwrite(output_path_radar, ARROW)


        screenshot_number += 1
        n +=1 
        sleep(0.3)
