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
                looked_folder = 'classification_data/attack_img/'
            except FileNotFoundError:
                print('file not found')
                df = create_df('classification_data/attack_img/attack_data.csv')
            except Exception as e:
                print(f"exception {e}")
            return looked_folder, df
        case 'attack_aug':
            try:
                df = pd.read_csv('augmented_data/attack_img/attack_data.csv')
                looked_folder = 'augmented_data/attack_img/'
            except FileNotFoundError:
                print('file not found')
                df = create_df('augmented_data/attack_img/attack_data.csv')
            except Exception as e:
                print(f"exception {e}")
            return looked_folder, df
        case 'explore':
            try:
                df = pd.read_csv('classification_data/explore_img/explore_data.csv')
                looked_folder = 'classification_data/explore_img/'
            except FileNotFoundError:
                print('file not found')
                df = create_df('classification_data/explore_img/explore_data.csv')
            except Exception as e:
                print(f"exception {e}")
            return looked_folder, df
        case 'explore_aug':
            try:
                df = pd.read_csv('augmented_data/explore_img/explore_data.csv')
                looked_folder = 'augmented_data/explore_img/'
            except FileNotFoundError:
                print('file not found')
                df = create_df('augmented_data/explore_img/explore_data.csv')
            except Exception as e:
                print(f"exception {e}")
            return looked_folder, df
        case 'getaway':
            try:
                df = pd.read_csv('classification_data/getaway_img/getaway_data.csv')
                looked_folder = 'classification_data/getaway_img/'
            except FileNotFoundError:
                print('file not found')
                df = create_df('classification_data/getaway_img/getaway_data.csv')
            except Exception as e:
                print(f"exception {e}")
            return looked_folder, df
        case 'loot':
            try:
                df = pd.read_csv('classification_data/loot_img/loot_data.csv')
                looked_folder = 'classification_data/loot_img/'
            except FileNotFoundError:
                print('file not found')
                df = create_df('classification_data/loot_img/loot_data.csv')
            except Exception as e:
                print(f"exception {e}")
            return looked_folder, df
def prediction_preparation(img):
    tbp = np.asarray(img)
    tbp = np.expand_dims(tbp, axis=0)
    return tbp

def reclassify(image_folder_explore, image_folder_attack, df_explore, df_attack, mode, model_predictor):
    cv2.namedWindow(f"Reclassifier", cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Reclassifier', 640, 360)

    looked_folder = image_folder_explore if mode == "explore" else image_folder_attack
    looked_df = df_explore if mode == "explore" else df_attack
    print(looked_folder)
    try:
        for filename in os.listdir(looked_folder):
            finish = False
            skip = False
            drop_df = False
            change_df = False


            if filename.endswith(".jpg") and not filename.startswith("checked_"):
                print(f'opened: {filename}')

                image = cv2.imread(looked_folder+filename)
                predictions = model_predictor.predict(prediction_preparation(image))[0].tolist()

                max_index = predictions.index(max(predictions))

                if max_index == 0 and mode == "attack":
                    print('thatss attack, continuing')
                    continue
                elif max_index == 1 and mode == "explore":
                    print('thats explore, continuing')
                    continue

                display = image

                cv2.putText(display, f"{looked_folder+filename}", (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                cv2.imshow('Reclassifier', display)

                key = cv2.waitKey(1) & 0xFF
                while key != ord('z'):
                    key = cv2.waitKey(1) & 0xFF

                    if key == ord('q') and mode != 'explore':
                        print(f'Replacing {looked_folder}{filename}, for {image_folder_explore + filename}')
                        os.replace(f'{looked_folder + filename}', f'{image_folder_explore + filename}')
                        drop_df = True
                        break
                    if key == ord('q') and mode == 'explore':
                        new_filename = 'checked_' + filename
                        print(f'Renaming {looked_folder}{filename}, for {image_folder_explore + new_filename}')
                        os.rename(looked_folder + filename, f'{image_folder_explore + new_filename}')
                        change_df = True
                        break
                        
                    if key == ord('a') and mode != 'attack':
                        print(f'Replacing {looked_folder + filename}, for {image_folder_attack + filename}')
                        os.replace(f'{looked_folder + filename}', f'{image_folder_attack + filename}')
                        drop_df = True
                        break

                    if key == ord('a') and mode == 'attack':
                        new_filename = 'checked_' + filename
                        print(f'Renaming {looked_folder}{filename}, for {image_folder_attack + new_filename}')
                        os.rename(looked_folder + filename, f'{image_folder_attack + new_filename}')
                        change_df = True
                        break
                    if key == ord('d'):
                        print(f'deleting {looked_folder + filename}')
                        os.remove(f'{looked_folder + filename}')
                        drop_df = True
                        break
                    if key == ord('x'):
                        finish = True
                        break


                if finish == True:
                    break
                if skip == True:
                    continue

                if drop_df == True:
                    print('trying to drop')
                    change_index = looked_df['filename'] == filename
                    if change_index.any():
                        change_index = looked_df.loc[change_index]
                        change_index = change_index.index[0]
                        looked_df = looked_df.drop(change_index)
                        df_savepath = looked_folder + ('explore_data.csv' if mode == 'explore' else 'attack_data.csv')
                        looked_df.to_csv(df_savepath, index=False)
                        print(f'saved {df_savepath}')
                    else:
                        print(f'not found {filename} in df')
                        
                if change_df == True:
                    print('trying to change')
                    change_index = looked_df['filename'] == filename
                    if change_index.any():
                        change_index = looked_df.loc[change_index]
                        change_index = change_index.index[0]

                        x,y = looked_df.loc[change_index]['x'], looked_df.loc[change_index]['y']

                        looked_df.loc[change_index] = [new_filename,x,y]
                        # print(looked_df.loc[change_index])

                        df_savepath = looked_folder + ('explore_data.csv' if mode == 'explore' else 'attack_data.csv')
                        looked_df.to_csv(df_savepath, index=False)
                        print(f'saved {df_savepath}')
                    else:
                        print(f'not found {filename} in df')


    except Exception as e:
        print(f"{e}")

    # df.to_csv(f"{looked_folder}/{label_type}_data.csv", index=False)


image_folder_explore, df_explore = path_acquisiton('explore_aug')
image_folder_attack, df_attack = path_acquisiton('attack_aug')
model_classifier = tf.keras.models.load_model('classificator_newgen_augment.h5')


### mode = target folder
reclassify(image_folder_explore, image_folder_attack, df_explore, df_attack, 'attack', model_classifier)


