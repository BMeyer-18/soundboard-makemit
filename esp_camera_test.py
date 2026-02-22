import cv2

url = "http://10.42.0.124/"
cap = cv2.VideoCapture(url)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    cv2.imshow("ESP32 Stream", frame)
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows