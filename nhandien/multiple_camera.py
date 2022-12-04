#!/usr/bin/env python
'''
Python code to test webcam. 
If the code doesn't run, change the webcamID to 0,1,2,3 etc
After seeing the webcam, press 'q' to stop the script
'''


import numpy as np
import cv2


#change webcamID to 0,1,2 etc depending on the type of camera
webcamID = 1
cap1 = cv2.VideoCapture(webcamID)


while(True):
    # Capture frame-by-frame
    ret1, frame1 = cap1.read()

    # Our operations on the frame come here
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    #gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('PRESS Q TO QUIT',gray1)
    #cv2.imshow('frame2',gray2)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap1.release()
cv2.destroyAllWindows()