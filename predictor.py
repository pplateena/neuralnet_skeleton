import utility_modules.move_ctype  as cici
from utility_modules.capture import capture_mode

import cv2
import numpy as np

import tensorflow as tf
import playsound
from time import sleep
from tensorflow.keras.optimizers import Adam
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
# tf.compat.v1.disable_eager_execution()
# tf.compat.v1.experimental.output_all_intermediates(True)


model_classifier = tf.keras.models.load_model('classificator_newgen_augment_gigadata.h5')
# model_classifier.compile(optimizer='adam',
#                   loss='categorical_crossentropy',
#                   metrics=['accuracy'])
print('loade model_class')
model_explorer = tf.keras.models.load_model('ME_gpu.h5')
# model_explorer.compile(loss='mean_squared_error', optimizer=Adam())

print('loade ME')
model_attacker = tf.keras.models.load_model('mouse_attack_fhd_normalized_gpu.h5', compile = False)
model_attacker.compile(loss='mean_squared_error', optimizer=Adam())
print('loade MA')
#
# attack_sound = 'classification_data/attack.mp3'
# explore_sound ='classification_data/explore.mp3'
# getaway_sound ='classification_data/getaway.mp3'
# loot_sound ='classification_data/loot.mp3'

last_three_preds = []


# for n in range(50):

while True:
    try:
        img = capture_mode('desired', (0,0,1920,1080))
        resized = cv2.resize(img,(640,360))

        tbp = np.asarray(resized)
        tbp = np.expand_dims(tbp, axis=0)
        print('trying')
        predictions = model_classifier.predict(tbp)[0].tolist()
        print(predictions)

        max_value = max(predictions)
        max_index = predictions.index(max_value)


        last_three_preds.append(max_index)

        if len(last_three_preds) == 5:
            last_three_preds.pop(0)

        if all(ele == 0 for ele in last_three_preds) and len(last_three_preds) == 4:
            print('before', max_index)
            max_index = 0 if max_index == 1 else 1
            last_three_preds[-1] = max_index
            print('after', max_index)

        if last_three_preds[-1] != max_index or (all(ele == [last_three_preds[-1]] for ele in last_three_preds) and len(last_three_preds) == 4):
            if max_index == 0:
                cici.release_left_button()
            if max_index == 1:
                cici.release_right_button()


        if max_index ==0:
            # playsound.playsound(attack_sound, block=False)
            print('attacking')
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
            # cici.release_right_button()

        elif max_index == 1:
            # playsound.playsound(explore_sound, block=True)
            print('exploring')
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


            print(x,y)
            cici.move_cursor_steps(x, y)
            cici.press_left_button()

            # sleep(0.5)
            # cici.release_left_button()
    except Exception as e:
        print(e)
