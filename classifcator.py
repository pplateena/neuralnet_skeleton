import cv2
import os
import pandas as pd

def draw_dot(image,button, x, y, radius=20, thickness=-1):
    color = (255, 0, 0) if button == "left" else (0, 0, 255)
    cv2.circle(image, (x, y), radius, color, thickness)

def create_df():
    df = pd.DataFrame(columns=["filename", "scalar_x", "scalar_y", "s_button"])

    df.to_csv("prep_data/image_data.csv", index=False)

# create_df()
def sort_data():
    folder_path = "prep_data/"
    killer = 0

    delete_list = []
    attack_list = []
    explore_list = []
    getaway_list = []
    loot_list = []
    proceed = True
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg"):
            image = cv2.imread(folder_path + filename)

            if image is not None:
                display = image
                cv2.namedWindow("rap", cv2.WINDOW_NORMAL)
                cv2.resizeWindow('rap', 1600, 900)
                cv2.putText(display, f'{filename}, q-explore, w-loot, a-attack, s-getaway', (50, 20), color = (255,255,255), fontFace = cv2.FONT_HERSHEY_COMPLEX, fontScale = 0.5, thickness = 1)
                cv2.imshow('rap', display)
                key = cv2.waitKey(0) & 0xFF

                if key == ord('a'):  #attack
                    cv2.waitKey(1)
                    print('attack')
                    attack_list.append(filename)
                elif key == ord('s'):  # getaway
                    cv2.waitKey(1)
                    print('getaway list')
                    getaway_list.append(filename)
                elif key == ord('q'): #explore
                    cv2.waitKey(1)
                    print('explore')
                    explore_list.append(filename)

                elif key == ord('w'): #loot
                    cv2.waitKey(1)
                    print('looting this')
                    loot_list.append(filename)
                elif key == ord('d'):
                    cv2.waitKey(1)
                    print('deleting this')
                    delete_list.append(filename)


                elif key == ord('k'):
                    print('killing window')
                    break
                elif key == ord('m'):
                    cv2.destroyWindow('rap')
                    print('fykcin blowin')
                    proceed = False
                    break
                killer += 1

        if killer == 150:
            break
    print(proceed)
    if proceed != False:
        for filename in delete_list:
            os.remove(f'prep_data/{filename}')
            print(f"Deleted {filename}")

        for filename in attack_list:
            os.replace(f'prep_data/{filename}', f'classification_data/attack_img/{filename}')
            print(f"Moved {filename} to attack_img")

        for filename in getaway_list:
            os.replace(f'prep_data/{filename}', f'classification_data/getaway_img/{filename}')
            print(f"Moved {filename} to getaway_img")

        for filename in explore_list:
            os.replace(f'prep_data/{filename}', f'classification_data/explore_img/{filename}')
            print(f"Moved {filename} to explore_img")

        for filename in loot_list:
            os.replace(f'prep_data/{filename}', f'classification_data/loot_img/{filename}')
    else:
        print('didnt change files')

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

sort_data()
# prepare_data()
# check_prep()