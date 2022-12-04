from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2

camera = PiCamera()
camera.rotation = 180
camera.resolution = (320, 240)
camera.framerate = 24
rawCapture = PiRGBArray(camera, size=(320, 240))
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True) :
    image = frame.array
    if cv2.waitKey(1) & 0xff == ord("q"):
        exit()
    image = cv2.flip(image, 1)
    cv2.imshow("check", image)
    rawCapture.truncate(0)
