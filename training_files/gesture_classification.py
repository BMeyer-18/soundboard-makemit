"""
Importing necessary modules:
- mediapipe: the runtime module for handling media processing
- time: used to track the duration of the video capture
- picamera2 (Pi) or cv2 (dev machine): camera capture, chosen automatically based on what's available
"""

from unittest import result

from play_audio import PlayAudio
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import time

try:
    from picamera2 import Picamera2
    USE_PICAMERA = True
except ImportError:
    import cv2
    USE_PICAMERA = False


class GestureClassifier():
    model_path = ""

    def __init__(self, model_path, min_confidence):
        self.model_path = model_path
        self.min_confidence = min_confidence
        self.base_options = mp.tasks.BaseOptions
        self.gesture_recognizer = mp.tasks.vision.GestureRecognizer
        self.gesture_recognizer_options = mp.tasks.vision.GestureRecognizerOptions
        self.vision_running_mode = mp.tasks.vision.RunningMode

    def setup_camera(self):
        if USE_PICAMERA:
            cam = Picamera2()
            config = cam.create_preview_configuration(main={"format": "RGB888","size": (640, 480)})
            cam.configure(config)
            cam.start()
            return cam
        else:
            return cv2.VideoCapture(0)
        
    def capture_frame(self, cam):
        if USE_PICAMERA:
            return cam.capture_array()
        else:
            ret, frame = cam.read()
            if not ret:
                return None
            return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    def release_camera(self, cam):
        if USE_PICAMERA:
            cam.stop()
        else:
            cam.release()

    def classify_image(self, cam, recognizer):
        player = PlayAudio()
        frame = self.capture_frame(cam)
        if frame is None:
            print("failed to capture image")
            return
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        gesture_recognition_result = recognizer.recognize(mp_image)
        classification = gesture_recognition_result.gestures
        if len(classification) > 0 and not classification[0][0].category_name == '':
            print(classification[0][0].category_name)
            print(classification[0][0].score)
            player.play_sound(classification[0][0].category_name)
            return classification[0][0].category_name
        return None

    def classify_live_footage(self, duration):
        options = self.gesture_recognizer_options(
            base_options=self.base_options(model_asset_path=self.model_path),
            running_mode=self.vision_running_mode.IMAGE,
            min_hand_detection_confidence=self.min_confidence,
            min_hand_presence_confidence=self.min_confidence)
        last_gesture = None
        with self.gesture_recognizer.create_from_options(options) as recognizer:
            cam = self.setup_camera()

            # begin video capture
            print("beginning video capture")
            start_time = time.time()
            while time.time() - start_time < duration:
                result = self.classify_image(cam, recognizer)
                if result != None:
                    last_gesture = result
            self.release_camera(cam)
        return last_gesture