import cv2
import numpy as np
import tensorflow as tf

from tensorflow.keras.optimizers import Adam
from utility_modules.capture import capture_mode
import utility_modules.move_ctype  as cici
import cv2
import numpy as np

import tensorflow as tf

from tensorflow.keras.optimizers import Adam

model_rap = tf.keras.models.load_model('C:\\Users\\platy_move\\Documents\\GitHub\\neuralnet_skeleton\\cemetery.h5')
model_rap.summary()

model_rap.compile(loss='mean_squared_error', optimizer=Adam())


for n in range(40):
    img = capture_mode('desired', (0,0,1920,1080))
    resized = cv2.resize(img,(640,360))
    tbp = np.asarray(resized)
    tbp = np.expand_dims(tbp, axis=0)

    prediction = model_rap.predict(tbp)
    print(prediction[0])
    x,y,button = round(prediction[0]*3), round(prediction[1]*3), prediction[0]

    cici.move_cursor_steps(x,y)

    if button >= 50:
        cici.press_right_button()
        sleep(0.1)
        cici.release_right_button()
    else:
        cici.press_left_button()
        sleep(0.1)
        cici.release_left_button()

