import cv2
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, MaxPooling2D, Conv2D, Flatten, Dense, Dropout
from tensorflow.keras.constraints import MaxNorm
from tensorflow.keras.optimizers import Adam

from tensorflow.keras.constraints import Constraint


def compile_model():
    image_width, image_height, channels = 640, 360, 3  # Assuming RGB images

    model = Sequential()
    model.add(Input(shape=(image_height, image_width, channels)))
    model.add(MaxPooling2D((2, 2)))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D((2, 2)))
    model.add(Flatten())
    model.add(Dense(64, activation='relu'))
    model.add(Dense(64, activation='relu'))

    model.add(Dense(64, activation='relu'))

    model.add(Dense(3, activation='linear'))

    model.compile(loss='mean_squared_error', optimizer=Adam())
    return model

def create_input():
    X = []
    y = []
    df = pd.read_csv("prep_data/resized_df.csv")

    shuffled_df = df.sample(len(df))

    print(shuffled_df.head)  # Shuffled DataFrame
    s = 0
    for entry in shuffled_df.values:
        s += 1
        # print(s)
        entry_img = cv2.imread(f"prep_data/{entry[0]}")

        prepared_y = np.delete(entry,0)

        X.append(entry_img)
        y.append(prepared_y)

    y = np.asarray(y).astype(np.float32)

    return X, y


def train_model(model, X, y, epochs_req):
    train_split = int(len(y) * 0.8)
    X_train, X_test = np.array(X[:train_split - 1]), np.array(X[train_split:])
    y_train, y_test = y[:train_split - 1], y[train_split:]


    model.fit(X_train, y_train, epochs=(epochs_req), validation_data=(X_test, y_test))

    for i in range(10):

        tbp = np.asarray(X_test[i])
        tbp = np.expand_dims(tbp, axis=0)
        predictions = model.predict(tbp)
        print("pred", predictions, "real", y_test[i])

    return model





# model = compile_model()

model_path = "low_res.h5"
X, y = create_input()

model = tf.keras.models.load_model(model_path)
model.summary()
model.compile(loss='mean_squared_error', optimizer=Adam())

model = train_model(model, X, y, 7)

model.save('low_res.h5')


# # Load the CSV file into a DataFrame
# df = pd.read_csv('prep_data/image_data.csv')
# print(df.head)
#
# df['scalar_x'] = df['scalar_x'] * 640
#
# # Rescale scalar_y to the range 0-1080
# df['scalar_y'] = df['scalar_y'] * 360
#
# df['s_button'] = df['s_button'] * 100
#
# print(df.head)
#
# # Save the updated DataFrame to a new CSV file
# df.to_csv('prep_data/resized_df.csv', index=False)