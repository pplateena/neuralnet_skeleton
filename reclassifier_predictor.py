import os

import numpy as np
import pandas as pd
import tensorflow as tf
import cv2

def path_acquisiton(mode):
    match mode:
        case 'attack':
            try:
                df = pd.read_csv('classification_data/attack_img/attack_data.csv')
                image_folder_path = 'classification_data/attack_img/'
            except FileNotFoundError:
                print('file not found')
                df = create_df('classification_data/attack_img/attack_data.csv')
            except Exception as e:
                print(f"exception {e}")
            return image_folder_path, df
        case 'attack_aug':
            try:
                df = pd.read_csv('augmented_data/attack_img/attack_data.csv')
                image_folder_path = 'augmented_data/attack_img/'
            except FileNotFoundError:
                print('file not found')
                df = create_df('augmented_data/attack_img/attack_data.csv')
            except Exception as e:
                print(f"exception {e}")
            return image_folder_path, df
        case 'explore':
            try:
                df = pd.read_csv('classification_data/explore_img/explore_data.csv')
                image_folder_path = 'classification_data/explore_img/'
            except FileNotFoundError:
                print('file not found')
                df = create_df('classification_data/explore_img/explore_data.csv')
            except Exception as e:
                print(f"exception {e}")
            return image_folder_path, df
        case 'explore_aug':
            try:
                df = pd.read_csv('augmented_data/explore_img/explore_data.csv')
                image_folder_path = 'augmented_data/explore_img/'
            except FileNotFoundError:
                print('file not found')
                df = create_df('augmented_data/explore_img/explore_data.csv')
            except Exception as e:
                print(f"exception {e}")
            return image_folder_path, df
        case 'getaway':
            try:
                df = pd.read_csv('classification_data/getaway_img/getaway_data.csv')
                image_folder_path = 'classification_data/getaway_img/'
            except FileNotFoundError:
                print('file not found')
                df = create_df('classification_data/getaway_img/getaway_data.csv')
            except Exception as e:
                print(f"exception {e}")
            return image_folder_path, df
        case 'loot':
            try:
                df = pd.read_csv('classification_data/loot_img/loot_data.csv')
                image_folder_path = 'classification_data/loot_img/'
            except FileNotFoundError:
                print('file not found')
                df = create_df('classification_data/loot_img/loot_data.csv')
            except Exception as e:
                print(f"exception {e}")
            return image_folder_path, df
def prediction_preparation(img):
    tbp = np.asarray(img)
    tbp = np.expand_dims(tbp, axis=0)
    return tbp
def label_photos(image_folder_path, df):


    label_type = image_folder_path.split('/')[1].split('_')[0]
    cv2.namedWindow("labeler", cv2.WINDOW_NORMAL)
    cv2.resizeWindow('labeler', 640, 360)
    def click_event(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            global image  # Access the global image variable within the function
            image = cv2.imread(param[0]).copy()  # Reload image copy on click
            clicked_coords[0] = (x, y)  # Update coordinates on click
            cv2.circle(image, (x, y), 10, (255, 0, 0), -1)
            cv2.imshow('labeler', image)

    s= 0
    try:
        for filename in os.listdir(image_folder_path):
            print(filename)
            finish = False
            skip = False
            drop_db = False
            if filename.endswith(".jpg"):
                print(f'opened: {filename}')
                cv2.setMouseCallback('labeler', click_event, param=[image_folder_path + filename])
                image = cv2.imread(image_folder_path+filename)


                clicked_coords = [(0, 0)]
                x, y = 0, 0


                cv2.imshow('labeler', image)
                key = cv2.waitKey(1) & 0xFF

                while key != ord('z'):
                    key = cv2.waitKey(1) & 0xFF
                    if x != clicked_coords[0][0] and y != clicked_coords[0][1]:
                        x, y = clicked_coords[0][0], clicked_coords[0][1]

                    if key == ord('q'):
                        os.replace(f'{image_folder_path}{filename}', f'augmented_data/explore_img/{filename}')
                        print(f'moved {filename}')
                        drop_db = True
                        break


                    if key == ord('a'):
                        os.replace(f'{image_folder_path}{filename}', f'augmented_data/attack_img/{filename}')
                        print(f'moved {filename}')
                        skip = True
                        break
                    if key == ord('d'):
                        os.remove(f'{image_folder_path}{filename}')
                        print(f"Deleted {filename}")
                        skip = True
                        break

                    if key == ord('x'):
                        finish = True
                        break

                # if finish == True:
                #     break
                # if skip == True:
                #     continue

                if drop_db == True:
                    row = df.loc[df['filename'] == filename]

                    df = df.drop(df[not row.empty].index)
                    print(df)



                s += 1
            if s == 100:
                break
    except Exception as e:
        print(f"{e}")

    # df.to_csv(f"{image_folder_path}/{label_type}_data.csv", index=False)



image_folder_path, df = path_acquisiton('attack')

label_photos(image_folder_path, df)

model_classifier = tf.keras.models.load_model('classificator_newgen_augment.h5')


# predictions = model_classifier.predict(tbp)[0].tolist()
