import cv2
import os
import pandas as pd
"""
THIS IS FIRST GENERATION OF CLASSIFIER, USED ONLY AS REFERENCE FOR FUTURE SCRIPTS.

"""
def create_df(saved_folder = 'prep_data'):
    """

    :param saved_folder: any specified folder, prep_data by default
    :return: creates a .csv dataframe with required format stored in specified location
    """
    df = pd.DataFrame(columns=["filename", "scalar_x", "scalar_y", "s_button"])
    df.to_csv(f"{saved_folder}/image_data.csv", index=False)
def parse_mfile(filename:str):
    """
    Function to return data captured from filename
    :param filename: string of filename which is worked on
    :return: mouse button that were pressed on given screenshot, x and y coordinates of mouse during screenshot

    Example: filename = 'mouse_button.RMB_960_540_1241247.png
    """

    parts = filename.split("_")
    if len(parts) != 5:
        return None
    side = parts[1].split(".")[1]
    x = int(parts[2])
    y = int(parts[3])

    return side, x, y
def scalar_mousepos(mx, my):
    """
    Function to convert mouse coordinates from monitor pixel range into scalar values
    :param mx:
    :param my:
    :return: scalar_mx, scalar_my: range(float(0,1))
    """
    scalar_mx, scalar_my = round(mx/1920, 4) ,round(my/1080, 4)
    return scalar_mx, scalar_my
def draw_dot(image,button, x, y, radius=20, thickness=-1):
    """
    Function to draw dot on running cv2 image besed on button pressed
    :param image: np.array() of image
    :param button: 'left' or 'right' str()
    :param x: int
    :param y: int
    :param radius: int
    :param thickness: int
    :return: None
    """
    color = (255, 0, 0) if button == "left" else (0, 0, 255)
    cv2.circle(image, (x, y), radius, color, thickness)
def sort_data(folder_path = "dataset/"):
    """
    Function to sort data by pressing buttons in cv2 window.
    Moves images to different folders based on key pressed.

    :param folder_path: path(str)
    :return: None
    """

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

def prepare_data(folder_path = "prep_data/", df = pd.read_csv("prep_data/image_data.csv")):
    """
    Function to prepare data. Resizes fhd images to 640x480 and saves them, appending new x, y values and
    pressed button information to dataframe
    :param folder_path: path(str)
    :param df: pandas dataframe
    :return:
    """
    counter = 2300 # used to skip certain amount of already saved photos to exclude conflicts

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

    df.to_csv(f"{folder_path}/image_data.csv", index=False)
def check_prep():
    """
    function to manually check whether stored images are relevant
    :return: None
    """
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

# create_df()

prepare_data()
sort_data()

# check_prep()
