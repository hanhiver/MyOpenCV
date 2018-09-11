import numpy as np
import cv2
import time

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect the faces in the frame.
    face_cascade = cv2.CascadeClassifier(r'./haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor = 1.15,
        minNeighbors = 5,
        minSize = (5, 5),
        flags = 2
        )

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+w), (0, 255, 0), 2)
        

    # Display the resulting frame
    cv2.imshow('frame', frame)

    time.sleep(0.1)

    print(gray.shape)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release capture
cap.release()
cv2.destroyAllWindows()
