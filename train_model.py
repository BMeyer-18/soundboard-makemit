import os
import tensorflow as tf
from mediapipe_model_maker import gesture_recognizer
import matplotlib.pyplot as plt

class TrainModel():
    train_data = None
    val_data = None
    test_data = None
    model = None
    
    def __init__(self, data_path, model_path):
        self.data_path = data_path
        self.model_path = model_path
        assert tf.__version__.startswith('2')
        
    def load_data(self, train_split_percent):
        data = gesture_recognizer.Dataset.from_folder(
            dirname=self.data_path,
            hparams=gesture_recognizer.HandDataPreprocessingParams()
        )
        self.train_data, rest_data = data.split(train_split_percent)
        self.val_data, self.test_data = rest_data.split(0.5)

    def train_model(self):
        hparams = gesture_recognizer.HParams(export_dir=self.model_path)
        options = gesture_recognizer.GestureRecognizerOptions(hparams=hparams)
        self.model = gesture_recognizer.GestureRecognizer.create(
            train_data=self.train_data,
            validation_data=self.val_data,
            options=options
        )
        self.model.export_model()

    def evaluate_performance(self):
        loss, acc = self.model.evaluate(self.test_data, batch_size=1)
        return loss, acc