# imports
print("importing libraries")
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import time

# load model
print("loading model")
model_path = "/home/bmeyer/Downloads/exported_model/gesture_recognizer.task"
BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
#GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode

# prepare model for live stream
#print("running model")
#def print_result(result, output_image, timestamp_ms):
#    print('gesture recognition result: {}'.format(result))

options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.IMAGE,
#    result_callback=print_result,
    min_hand_detection_confidence=0.2,
    min_hand_presence_confidence=0.2)
with GestureRecognizer.create_from_options(options) as recognizer:
    # set up video capture from webcam
    print("setting up video capture")
    cam = cv2.VideoCapture(0)
    #frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    #frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
    #fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    #out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (frame_width, frame_height))
    
    # begin video capture
    print("beginning video capture")
    start_time = time.time()
    while time.time() - start_time < 30:
        ret, frame = cam.read()
        if ret:
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
            gesture_recognition_result = recognizer.recognize(mp_image)
            if len(gesture_recognition_result.gestures) > 0:
                print(gesture_recognition_result.gestures[0][0].category_name)
                print(gesture_recognition_result.gestures[0][0].score)
        else:
            print("failed to capture image")
    cam.release()
    cv2.destroyAllWindows()