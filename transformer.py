import cv2
import os
import pandas as pd
def scalar_mousepos(mx, my):
    # mx, my = position()
    scalar_mx, scalar_my = round(mx/1920, 4) ,round(my/1080, 4)
    return scalar_mx, scalar_my

def parse_mfile(filename):


    parts = filename.split("_")
    if len(parts) != 5:
        return None
    side = parts[1].split(".")[1]
    x = int(parts[2])
    y = int(parts[3])

    return side, x, y

def draw_dot(image,button, x, y, radius=20, thickness=-1):
    color = (255, 0, 0) if button == "left" else (0, 0, 255)
    cv2.circle(image, (x, y), radius, color, thickness)




def sort_data():
    folder_path = "dataset/"
    killer = 0

    delete_list = []
    approve_list = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg") and filename.startswith("M_Button"):

            button, x, y = parse_mfile(filename)
            print(button, x, y, filename)
            image_path = os.path.join(folder_path, filename)
            image = cv2.imread(image_path)

            if image is not None:
                display = image
                draw_dot(display, button, x, y)
                font = cv2.FONT_HERSHEY_SIMPLEX  # Choose a font (e.g., FONT_HERSHEY_PLAIN)
                color = (255, 0, 0)  # Blue color in BGR format
                font_scale = 1
                thickness = 2

                cv2.putText(display, button, (x, y), font, 2, (255, 255, 255), thickness)
                cv2.namedWindow("rap", cv2.WINDOW_NORMAL)
                cv2.resizeWindow('rap', 1600, 900)
                cv2.imshow('rap', display)
                key = cv2.waitKey(0) & 0xFF

                if key == ord('a'):  #appove
                    cv2.waitKey(1)
                    print('approving')
                    approve_list.append(filename)
                elif key == ord('e'): #erase
                    cv2.waitKey(1)
                    print('erasing')
                    delete_list.append(filename)
                elif key == ord('s'): #skip
                    cv2.waitKey(1)
                    print('skipping this')
                elif key == ord('k'):
                    print('killing window')
                    break

                killer += 1

        if killer == 150:
            break
    cv2.destroyWindow('rap')

    for filename in delete_list:
        os.remove(f'dataset/{filename}')
        print(f"Deleted {filename}")

    for filename in approve_list:

        os.replace(f'dataset/{filename}', f'prep_data/{filename}')  # Use replace for move functionality
        print(f"Moved {filename} to prep_data")
# sort_data()
def create_df():
    df = pd.DataFrame(columns=["filename", "scalar_x", "scalar_y", "s_button"])
    df.to_csv("prep_data/image_data.csv", index=False)

create_df()
def prepare_data():
    folder_path = "prep_data/"
    df = pd.read_csv("prep_data/image_data.csv")

    counter = len(df)+7000
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg") and filename.startswith("M_"):
            button, x, y = parse_mfile(filename)
            print(button, x, y, filename)
            image_path = os.path.join(folder_path, filename)
            image = cv2.imread(image_path)
            resized_image = cv2.resize(image, (640, 360))
            cv2.imwrite(folder_path + filename, resized_image)
            scalar_x, scalar_y = round(x/3), round(y/3),
            s_button = 0 if button == "left" else 100
            print(scalar_x, scalar_y,s_button, filename)

            df.loc[counter] = [f'{counter}.jpg', scalar_x, scalar_y, s_button]
            os.rename(f'prep_data/{filename}', f'prep_data/{counter}.jpg')
            counter += 1

    df.to_csv("prep_data/image_data.csv", index=False)
prepare_data()

def check_prep():
    folder_path = "prep_data/"
    df = pd.read_csv("prep_data/image_data.csv")
    print(df)
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg"):
            df_index = int(filename.split(".")[0])
            _,scalar_x, scalar_y, s_button = df.loc[df_index]
            print(scalar_x, scalar_y,s_button)
            x, y, button = round(scalar_x*640), round(scalar_y*360), "left" if s_button == 0 else "right"
            print(x, y, button)
            image = cv2.imread(folder_path + filename)
            if image is not None:
                display = image
                draw_dot(display, button, x, y)

                cv2.imshow('rap', display)
                key = cv2.waitKey(0) & 0xFF

# check_prep()