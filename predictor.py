import utility_modules.move_ctype  as cici
from utility_modules.capture import capture_mode

import cv2
import numpy as np

import tensorflow as tf
import playsound
from time import sleep
from tensorflow.keras.optimizers import Adam


with tf.device('CPU:0'):
    model_classifier = tf.keras.models.load_model('classificator_newgen_augment_gpu.h5', compile = False)
    model_classifier.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    model_explorer = tf.keras.models.load_model('mouse_explore_fhd_normalized_gpu.h5', compile = False)
    model_explorer.compile(loss='mean_squared_error', optimizer=Adam())
    model_attacker = tf.keras.models.load_model('mouse_attack_fhd_normalized_gpu.h5', compile = False)
    model_attacker.compile(loss='mean_squared_error', optimizer=Adam())

#
# attack_sound = 'classification_data/attack.mp3'
# explore_sound ='classification_data/explore.mp3'
# getaway_sound ='classification_data/getaway.mp3'
# loot_sound ='classification_data/loot.mp3'

last_three_preds = []
# img = capture_mode('desired', (0, 0, 1920, 1080))
# resized = cv2.resize(img, (640, 360))
# hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)
# cv2.imshow('hsv',hsv); cv2.waitKey(0)
# print(hsv.shape)

for n in range(50):

# while True:
    img = capture_mode('desired', (0,0,1920,1080))
    resized = cv2.resize(img,(640,360))

    tbp = np.asarray(resized)
    tbp = np.expand_dims(tbp, axis=0)
    predictions = model_classifier.predict(tbp)[0].tolist()
    print(predictions)

    max_value = max(predictions)
    max_index = predictions.index(max_value)


    # if predictions[0] < 0.6:
    #     max_index = 1
    last_three_preds.append(max_index)

    if len(last_three_preds) == 5:
        last_three_preds.pop(0)

    if all(ele == 0 for ele in last_three_preds) and len(last_three_preds) == 4:
        print('before', max_index)
        max_index = 0 if max_index == 1 else 1
        last_three_preds[-1] = max_index
        print('after', max_index)
    #
    # if last_three_preds[-1] != max_index or (all(ele == [last_three_preds[-1]] for ele in last_three_preds) and len(last_three_preds) == 4):
    #     if max_index == 0:
    #         cici.release_left_button()
    #     if max_index == 1:
    #         cici.release_right_button()


    if max_index ==0:
        # playsound.playsound(attack_sound, block=False)

        predictions = model_attacker.predict(tbp)[0].tolist()
        x, y = int(predictions[0]), int(predictions[0])

        if x <= 960:
            x = 960 + x
        else:
            x = x + 960

        if y <= 540:
            y = 540 + y
        else:
            y = y + 540

        print(x,y)

        cici.move_cursor_steps(x,y)
        cici.press_right_button()
        # sleep(0.1)
        cici.release_right_button()

    elif max_index == 1:
        # playsound.playsound(explore_sound, block=True)

        predictions = model_explorer.predict(tbp)[0].tolist()
        x,y = int(predictions[0]),int(predictions[1])
        print('before', x,y)
        if x <= 960:
            x = 960 + x
        else:
            x = x + 960

        if y <= 540:
            y = 540 + y
        else:
            y = y + 540

        #
        print(x,y)
        cici.press_left_button()
        cici.move_cursor_steps(x,y)
        # sleep(0.5)
        cici.release_left_button()


    # sleep(1)
