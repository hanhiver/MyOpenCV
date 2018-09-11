import numpy as np
import cv2
import time

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # cv2.rectangle(gray,(300,300),(800,700),(0,255,0),2)
        

    # Display the resulting frame
    cv2.imshow('frame', gray)

    time.sleep(0.3)

    print(gray.shape)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release capture
cap.release()
cv2.destroyAllWindows()
