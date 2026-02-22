from play_audio import PlayAudio
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import time

class GestureClassifier():
    model_path = ""
    
    def __init__(self, model_path, min_confidence):
        self.model_path = model_path
        self.min_confidence = min_confidence
        self.BaseOptions = mp.tasks.BaseOptions
        self.GestureRecognizer = mp.tasks.vision.GestureRecognizer
        self.GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
        self.VisionRunningMode = mp.tasks.vision.RunningMode
        
    def classify_image(self, cam, recognizer):
        player = PlayAudio()
        ret, frame = cam.read()
        if ret:
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
            gesture_recognition_result = recognizer.recognize(mp_image)
            classification = gesture_recognition_result.gestures
            if len(classification) > 0 and not classification[0][0].category_name == '':
                print(classification[0][0].category_name)
                print(classification[0][0].score)
                player.play_sound(classification[0][0].category_name)
                
        else:
            print("failed to capture image")

    def classify_live_footage(self, duration):
        options = self.GestureRecognizerOptions(
            base_options=self.BaseOptions(model_asset_path=self.model_path),
            running_mode=self.VisionRunningMode.IMAGE,
            min_hand_detection_confidence=self.min_confidence,
            min_hand_presence_confidence=self.min_confidence)
        with self.GestureRecognizer.create_from_options(options) as recognizer:
            cam = cv2.VideoCapture(0)
            
            # begin video capture
            print("beginning video capture")
            start_time = time.time()
            while time.time() - start_time < duration:
                self.classify_image(cam, recognizer)
            cam.release()
            cv2.destroyAllWindows()
