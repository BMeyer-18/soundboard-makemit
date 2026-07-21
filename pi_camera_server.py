"""
Requires apt install picamera2/libcamera2-dev for Raspberry Pi OS.
Provides instructions for the camera to funcntion over a Unix socket, which is required for the Pi Camera to work with the mediapipe gesture recognition model.
If using cv2 on a dev machine for camera capture, this file is not required.
"""

import socket
import struct
import os
from picamera2 import Picamera2

SOCK_PATH = "/tmp/soundboard_camera.sock" # Path to the socket file on the Raspberry Pi

def main():
    # Check if the socket file already exists and remove it if it does as to avoid errors.
    if os.path.exists(SOCK_PATH):
        os.remove(SOCK_PATH)
    # Configures the Pi Camera to capture RGB images at 640x480 resolution and serve them over a Unix socket.
    cam = Picamera2()
    config = cam.create_preview_configuration(main={"format": "RGB888", "size": (640, 480)})
    cam.configure(config)
    cam.start()

    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(SOCK_PATH)
    server.listen(1)
    os.chmod(SOCK_PATH, 0o666)  # allow the pyenv process to connect
    print(f"Camera server listening on {SOCK_PATH}")

    try:
        while True:
            conn, _ = server.accept()
            print("Client connected")
            with conn:
                try:
                    while True:
                        request = conn.recv(1)
                        if not request:
                            break  # client disconnected
                        if request == b"F":
                            frame = cam.capture_array()  # numpy array, H x W x 3
                            frame = frame[:, :, ::-1]  # BGR -> RGB
                            h, w = frame.shape[0], frame.shape[1]
                            data = frame.tobytes()
                            header = struct.pack("!III", w, h, len(data))
                            conn.sendall(header + data)
                except (BrokenPipeError, ConnectionResetError):
                    print("Client disconnected")
    finally:
        cam.stop()
        server.close()
        if os.path.exists(SOCK_PATH):
            os.remove(SOCK_PATH)

if __name__ == "__main__":
    main()
