
from utility_modules.capture import capture_mode

import cv2
import numpy as np

import tensorflow as tf
import playsound
from time import sleep

model_rap = tf.keras.models.load_model('class_2.h5')
# model_rap.summary()

attack_sound = 'classification_data/attack.mp3'
explore_sound ='classification_data/explore.mp3'
getaway_sound ='classification_data/getaway.mp3'
loot_sound ='classification_data/loot.mp3'

for n in range(100):
    img = capture_mode('desired', (0,0,1920,1080))
    resized = cv2.resize(img,(640,360))

    tbp = np.asarray(resized)
    tbp = np.expand_dims(tbp, axis=0)
    predictions = model_rap.predict(tbp)[0].tolist()
    print(predictions)

    max_value = max(predictions)
    max_index = predictions.index(max_value)
    #
    # if predictions[1] >= 0.5 or predictions[2] >= 0.5 or predictions[3] >= 0.5:
    #     print('run')
    #     playsound.playsound(explore_sound, block=True)
    # elif predictions[0] >= 0.8:
    #     print('hit')
    #     playsound.playsound(attack_sound, block=True)
    # else:
    #     playsound.playsound(explore_sound, block=True)

    match max_index:

        case 0:
            playsound.playsound(attack_sound, block=True)
        case 1:
            playsound.playsound(explore_sound, block=True)
        case 2:
            playsound.playsound(loot_sound, block=True)
        case 3:
            playsound.playsound(getaway_sound, block=True)
        case _:
            print('ss')
    # sleep(1)


