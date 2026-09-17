from unittest import result
import time
import os
import socket
import struct
import numpy as np
from play_audio import PlayAudio
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

SOCK_PATH = "/tmp/soundboard_camera.sock"

class CameraSocketClient:
    """Connects to camera_server.py (system Python process) and requests frames."""

    def __init__(self, sock_path=SOCK_PATH):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.connect(sock_path)

    def get_frame(self):
        self.sock.sendall(b"F")
        header = self._recv_exact(12)
        w, h, length = struct.unpack("!III", header)
        data = self._recv_exact(length)
        return np.frombuffer(data, dtype=np.uint8).reshape((h, w, 3))

    def _recv_exact(self, n):
        buf = b""
        while len(buf) < n:
            chunk = self.sock.recv(n - len(buf))
            if not chunk:
                raise ConnectionError("Camera server disconnected")
            buf += chunk
        return buf

    def close(self):
        self.sock.close()

# Decide capture method and falls back to OpenCV dev machine, where camera_server.py
# isn't running and there's a normal USB webcam instead.
USE_SOCKET_CAMERA = os.path.exists(SOCK_PATH)
if not USE_SOCKET_CAMERA:
    import cv2

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
        if USE_SOCKET_CAMERA:
            return CameraSocketClient()
        else:
            return cv2.VideoCapture(0)

    def capture_frame(self, cam):
        if USE_SOCKET_CAMERA:
            try:
                return cam.get_frame()
            except ConnectionError:
                return None
        else:
            ret, frame = cam.read()
            if not ret:
                return None
            return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    def release_camera(self, cam):
        if USE_SOCKET_CAMERA:
            cam.close()
        else:
            cam.release()

    def classify_image(self, cam, recognizer):
        player = PlayAudio()
        frame = self.capture_frame(cam)
        if frame is None:
            print("failed to capture image")
            return
        # --- TEMPORARY DEBUG; to save frames as images for testing ---
        from PIL import Image
        Image.fromarray(frame).save("/tmp/debug_frame.jpg")
        # -------------------------------------------------------------
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
            print("beginning video capture")
            start_time = time.time()
            while time.time() - start_time < duration:
                result = self.classify_image(cam, recognizer)
                if result != None:
                    last_gesture = result
            self.release_camera(cam)
        return last_gesture
    