import cv2
import os
import numpy as np
import tensorflow as tf

from sklearn.model_selection import train_test_split
from tensorflow.keras import layers, models

IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43


def load_data(data_dir):
    images = []
    labels = []

    # Loop through each category folder
    for label in range(NUM_CATEGORIES):
        folder = os.path.join(data_dir, str(label))

        # Loop through each image file
        for file in os.listdir(folder):
            path = os.path.join(folder, file)

            # Read image
            img = cv2.imread(path)

            # Resize to required size
            img = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))

            images.append(img)
            labels.append(label)

    return np.array(images), np.array(labels)


def get_model():
    model = models.Sequential()

    # Convolutional layers
    model.add(layers.Conv2D(32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(layers.Conv2D(64, (3, 3), activation="relu"))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(layers.Flatten())

    # Hidden layer
    model.add(layers.Dense(128, activation="relu"))
    model.add(layers.Dropout(0.5))

    # Output layer
    model.add(layers.Dense(NUM_CATEGORIES, activation="softmax"))

    # Compile model
    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model