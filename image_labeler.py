import cv2
import os
import pandas as pd

def create_df(df_name):
    df = pd.DataFrame(columns=["filename", "x", "y"])
    df.to_csv(df_name, index=False)

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


def label_photos(image_folder_explore, image_folder_attack, df_explore, df_attack, mode):

    label_type = mode
    print(f'started labeling for: {label_type}')
    looked_folder = image_folder_explore if mode == "explore" else image_folder_attack
    looked_df = df_explore if mode == "explore" else df_attack
    for entry in looked_df['filename']:
        if entry.startswith('explore_') or entry.startswith('checked_explore_'):

            saving_index = entry.split('.')[0].split('_')[-1]
            saving_index = int(saving_index) + 1



    cv2.namedWindow("labeler", cv2.WINDOW_NORMAL)
    cv2.resizeWindow('labeler', 640, 360)
    def click_event(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            global image  # Access the global image variable within the function
            image = cv2.imread(param[0]).copy()  # Reload image copy on click
            clicked_coords[0] = (x, y)  # Update coordinates on click
            cv2.circle(image, (x, y), 10, (255, 0, 0), -1)
            cv2.imshow('labeler', image)


    try:
        print(looked_folder)
        for filename in os.listdir(looked_folder):
            finish = False
            drop_df = False
            append_df = False

            if filename.endswith(".jpg") and not filename.startswith(label_type):

                change_index = looked_df['filename'] == filename
                if change_index.any():
                    continue

                print(f'opened: {filename}')
                cv2.setMouseCallback('labeler', click_event, param=[looked_folder + filename])
                image = cv2.imread(looked_folder+filename)

                clicked_coords = [(0, 0)]
                x, y = 0, 0

                cv2.imshow('labeler', image)



                key = cv2.waitKey(1) & 0xFF
                while key != ord('z'):
                    key = cv2.waitKey(1) & 0xFF

                    if x != clicked_coords[0][0] and y != clicked_coords[0][1]:
                        x, y = clicked_coords[0][0], clicked_coords[0][1]



                    if key == ord('q') and mode != 'explore':
                        print(f'Replacing {looked_folder}{filename}, for {image_folder_explore + filename}')
                        os.replace(f'{looked_folder + filename}', f'{image_folder_explore + filename}')
                        drop_df = True
                        break
                    if key == ord('a') and mode != 'attack':
                        print(f'Replacing {looked_folder + filename}, for {image_folder_attack + filename}')
                        os.replace(f'{looked_folder + filename}', f'{image_folder_attack + filename}')
                        drop_df = True
                        break

                    if key == ord('d'):
                        print(f'deleting {looked_folder + filename}')
                        os.remove(f'{looked_folder + filename}')
                        drop_df = True
                        break

                    if key == ord('x'):
                        finish = True
                        break
                else:
                    append_df = True

                if finish == True:
                    break

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

                if append_df == True:
                    print('trying to append')
                    append_index = len(looked_df)

                    new_filename = mode + '_' + str(saving_index) + '.jpg'
                    saving_index += 1
                    looked_df.loc[append_index] = [new_filename,x,y]

                    print(f'changed name for: {filename}, to: {new_filename}')
                    os.rename(f'{looked_folder + filename}', f'{looked_folder + new_filename}')
                    df_savepath = looked_folder + ('explore_data.csv' if mode == 'explore' else 'attack_data.csv')
                    looked_df.to_csv(df_savepath, index=False)
                    print(f'saved {df_savepath}')
                else:
                    print(f'not found {filename} in df')

    except Exception as e:
        print(f"{e}")

def relabeler_afterpred(image_folder_explore, image_folder_attack, df_explore, df_attack, looked_folder):
    print(f'started labeling for relabeler')
    def saving_indexes(df_attack, df_explore):
        attack_last_index = len(df_explore) + 1
        explore_last_index = len(df_explore) + 1
        return attack_last_index, explore_last_index

    attack_last_index, explore_last_index = saving_indexes(df_attack, df_explore)

    cv2.namedWindow("labeler", cv2.WINDOW_NORMAL)
    cv2.resizeWindow('labeler', 640, 360)

    global change_df_explore
    change_df_explore = False

    global change_df_attack
    change_df_attack = False
    def click_event(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            # global img_clone  # Access the global image variable within the function
            img_clone = cv2.imread(param[0]).copy()  # Reload image copy on click
            clicked_coords[0] = (x, y)  # Update coordinates on click

            global change_df_attack,change_df_explore

            if change_df_attack:
                change_df_explore = True
                change_df_attack = False
            else:
                change_df_explore = True

            print(change_df_attack, change_df_explore)

            cv2.circle(img_clone, (x, y), 10, (255, 255, 0), -1)
            cv2.imshow('labeler', img_clone)

        if event == cv2.EVENT_RBUTTONDOWN:
            # global img_clone  # Access the global image variable within the function
            img_clone = cv2.imread(param[0]).copy()  # Reload image copy on click
            clicked_coords[0] = (x, y)  # Update coordinates on click

            # global change_df_attack, change_df_explore

            if change_df_explore:
                change_df_explore = False
                change_df_attack = True
            else:
                change_df_attack = True

            print(change_df_attack, change_df_explore)


            cv2.circle(img_clone, (x, y), 10, (0, 255, 255), -1)
            cv2.imshow('labeler', img_clone)


    try:
        print(looked_folder)
        for filename in os.listdir(looked_folder):
            finish = False

            change_df_explore = False
            change_df_attack = False

            append_df = False

            if filename.endswith(".jpg"):
                clicked_coords = [(0, 0)]
                x, y = 0, 0

                print(f'opened: {filename}')
                cv2.setMouseCallback('labeler', click_event, param=[looked_folder + filename])
                image = cv2.imread(looked_folder+filename)
                img_clone = image

                pred_x, pred_y = int(int(filename.split("_")[1]) / 3), int(int(filename.split("_")[2].split('.')[0]) / 3)
                color = (0,0,255) if filename.split("_")[0] == "attack" else (255,0,255)
                print(pred_x, pred_y)
                cv2.circle(img_clone, (pred_x, pred_y),10, color, -1)





                cv2.imshow('labeler', img_clone)
                key = cv2.waitKey(1) & 0xFF
                while key != ord('z'):
                    key = cv2.waitKey(1) & 0xFF

                    if x != clicked_coords[0][0] and y != clicked_coords[0][1]:
                        x, y = clicked_coords[0][0], clicked_coords[0][1]

                    if key == ord('q'):
                        print(f'Replacing {looked_folder}{filename}, to explore')
                        # os.replace(f'{looked_folder + filename}', f'{image_folder_explore + filename}')
                        change_df_explore = True

                    if key == ord('a'):
                        print(f'Replacing {looked_folder + filename}, for {image_folder_attack + filename}')
                        # os.replace(f'{looked_folder + filename}', f'{image_folder_attack + filename}')
                        change_df_attack = True


                    if key == ord('d'):
                        print(f'deleting {looked_folder + filename}')
                        os.remove(f'{looked_folder + filename}')
                        break

                    if key == ord('x'):
                        finish = True
                        break

                else:
                    append_df = True

                if finish == True:
                    break

                print(change_df_explore, change_df_attack)
                if append_df == True:
                    print('trying to append')

                    if change_df_explore:
                        append_index = len(df_explore)

                        new_filename = "explore_" + str(explore_last_index) + '.jpg'
                        explore_last_index += 1
                        df_explore.loc[append_index] = [new_filename,x,y]

                        print(f' replaced: {filename}, to: {new_filename}')
                        os.replace(f'{looked_folder + filename}', f'{image_folder_explore + new_filename}')
                        df_savepath = image_folder_explore + 'explore_data.csv'
                        df_explore.to_csv(df_savepath, index=False)

                        print(f'saved {df_savepath}')
                    elif change_df_attack:
                        append_index = len(df_attack)

                        new_filename = "attack_" + str(attack_last_index) + '.jpg'
                        attack_last_index += 1
                        df_attack.loc[append_index] = [new_filename,x,y]

                        print(f' replaced: {filename}, to: {new_filename}')
                        os.replace(f'{looked_folder + filename}', f'{image_folder_attack + new_filename}')
                        df_savepath = image_folder_attack + 'attack_data.csv'
                        df_attack.to_csv(df_savepath, index=False)

                        print(f'saved {df_savepath}')
                else:
                    print(f'not found {filename} in df')

    except Exception as e:
        print(f"{e}")
#
# image_folder_explore, df_explore = path_acquisiton('explore')
# image_folder_attack, df_attack = path_acquisiton('attack')

### mode = target folder
# label_photos(image_folder_explore, image_folder_attack, df_explore, df_attack, 'explore')

looked_folder = 'predicted_data/'

df_explore = pd.read_csv(f'{looked_folder}/explore_img/explore_data.csv')
df_attack = pd.read_csv(f'{looked_folder}/attack_img/attack_data.csv')

relabeler_afterpred(f'{looked_folder}explore_img/', f'{looked_folder}attack_img/',
                    df_explore, df_attack, looked_folder)