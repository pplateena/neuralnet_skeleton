import cv2
import os
import pandas as pd

# img = cv2.imread('classification_data/attack_img/7021.jpg')

# def click_event(event, x, y, flags, param):
#     if event == cv2.EVENT_LBUTTONDOWN:  # Check for left mouse button click
#         print(f"Left click coordinates: x = {x}, y = {y}")
#
#         font = cv2.FONT_HERSHEY_SIMPLEX



# cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
# cv2.resizeWindow('Image', 640, 360)
# cv2.setMouseCallback('Image', click_event)
#
#
# cv2.imshow('Image', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

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


def label_photos(image_folder_path, df):
    cv2.namedWindow("labeler", cv2.WINDOW_NORMAL)
    cv2.resizeWindow('labeler', 640, 360)


    def click_event(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            global image  # Access the global image variable within the function
            image = cv2.imread(param[0]).copy()  # Reload image copy on click
            clicked_coords[0] = (x, y)  # Update coordinates on click
            cv2.circle(image, (x, y), 10, (255, 0, 0), -1)
            cv2.imshow('labeler', image)


    for filename in os.listdir(image_folder_path):

        if filename.endswith(".jpg") and not filename.startswith('attack'):
            print(filename)
            cv2.setMouseCallback('labeler', click_event, param=[image_folder_path + filename])
            image = cv2.imread(image_folder_path+filename)


            clicked_coords = [(0, 0)]
            x, y = 0, 0


            cv2.imshow('labeler', image)

            while cv2.waitKey(1) & 0xFF != ord('z'):

                if x != clicked_coords[0][0] and y != clicked_coords[0][1]:
                    print('yup')
                    x, y = clicked_coords[0][0], clicked_coords[0][1]
                    # cv2.circle(image, (x, y), 10, (255, 255, 255), -1)



            print(x,y)





image_folder_path, df = path_acquisiton('attack')

print(image_folder_path, df)

label_photos(image_folder_path, df)