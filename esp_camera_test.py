import cv2

#url = "http://Nook Rats:NookRats!@10.42.0.124"
url = 0
cap = cv2.VideoCapture(url)
print('starting capture')
while True:
    ret, frame = cap.read()
    if not ret:
        print('failure')
        break
    print('showing stream')
    cv2.imshow("ESP32 Stream", frame)
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows
print('done')