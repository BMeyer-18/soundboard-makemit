# imports
print("importing libraries")
import os
import tensorflow as tf
assert tf.__version__.startswith('2')
from mediapipe_model_maker import gesture_recognizer

import matplotlib.pyplot as plt

# load, split data (80/10/10)
print("performing data split")
data_path = "/home/bmeyer/Downloads/rps_data_sample/"

data = gesture_recognizer.Dataset.from_folder(
    dirname=data_path,
    hparams=gesture_recognizer.HandDataPreprocessingParams()
)
train_data, rest_data = data.split(0.8)
val_data, test_data = rest_data.split(0.5)

# train model
print("training model")
hparams = gesture_recognizer.HParams(export_dir="/home/bmeyer/Downloads/exported_model")
options = gesture_recognizer.GestureRecognizerOptions(hparams=hparams)
model = gesture_recognizer.GestureRecognizer.create(
    train_data=train_data,
    validation_data=val_data,
    options=options
)

# evaluate model performance
print("evaluating model performance")
loss, acc = model.evaluate(test_data, batch_size=1)
print(f"Test loss:{loss}, Test Accuracy:{acc}")

# export model
print("exporting model")
model.export_model()