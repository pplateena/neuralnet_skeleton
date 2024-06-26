import cv2
import os

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





folder_path = "dataset/"
killer = 0

delete_list = []
approve_list = []

for filename in os.listdir(folder_path):
    if filename.endswith(".jpg") and filename.startswith("M_"):

        button, x, y = parse_mfile(filename)
        print(button, x, y, filename)
        image_path = os.path.join(folder_path, filename)
        image = cv2.imread(image_path)

        if image is not None:
            display = image
            draw_dot(display, button, x, y)

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

    if killer == 10:
        break
cv2.destroyWindow('rap')

for filename in delete_list:
    os.remove(f'dataset/{filename}')
    print(f"Deleted {filename}")


for filename in approve_list:

    os.replace(f'dataset/{filename}', f'prep_data/{filename}')  # Use replace for move functionality
    print(f"Moved {filename} to prep_data")




