import utility_modules.move_ctype  as cici
from utility_modules.capture import capture_mode

import cv2
import numpy as np

import tensorflow as tf
import playsound
from time import sleep

model_classifier = tf.keras.models.load_model('class_2.h5')
model_explorer = tf.keras.models.load_model('mouse_explore_2.h5')
model_attacker = tf.keras.models.load_model('mouse_attack.h5')


attack_sound = 'classification_data/attack.mp3'
explore_sound ='classification_data/explore.mp3'
getaway_sound ='classification_data/getaway.mp3'
loot_sound ='classification_data/loot.mp3'

for n in range(100):
    img = capture_mode('desired', (0,0,1920,1080))
    resized = cv2.resize(img,(640,360))

    tbp = np.asarray(resized)
    tbp = np.expand_dims(tbp, axis=0)
    predictions = model_classifier.predict(tbp)[0].tolist()
    print(predictions)

    max_value = max(predictions)
    max_index = predictions.index(max_value)

    if max_index == 2:
        max_index = 1
    elif max_index == 3:
        max_index = 1


    match max_index:
        case 0:
            playsound.playsound(attack_sound, block=False)

            predictions = model_attacker.predict(tbp)[0].tolist()
            x,y = int(predictions[0]*3),int(predictions[1]*3)
            cici.move_cursor_steps(x,y)
            cici.press_right_button()
            cici.release_right_button()

        case 1:
            playsound.playsound(explore_sound, block=True)

            predictions = model_attacker.predict(tbp)[0].tolist()
            x,y = int(predictions[0]*3),int(predictions[1]*3)
            print(x,y)
            cici.move_cursor_steps(x,y)
            cici.press_left_button()
            cici.release_left_button()
        case 2:
            playsound.playsound(loot_sound, block=True)
        case 3:
            playsound.playsound(getaway_sound, block=True)
        case _:
            print('ss')
    # sleep(1)


