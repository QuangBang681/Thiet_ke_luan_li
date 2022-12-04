from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
GPIO.setup(26, GPIO.OUT)

def unlock():
    GPIO.output(26, 1)
    #relay
    #print
def lock():
    GPIO.output(26, 0)
    
lock()
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
#camera.rotation = 180
camera.resolution = (400, 300)
camera.framerate = 24
rawCapture = PiRGBArray(camera, size=(400, 300))
#use Local Binary Patterns Histograms
recognizer = cv2.face.LBPHFaceRecognizer_create()
#Load a trainer file
recognizer.read('/home/pi/Desktop/Face_recognition/trainer/trainer.yml')
#Load a cascade file for detecting faces
face_cascade = cv2.CascadeClassifier('/home/pi/Desktop/Face_recognition/haarcascade_frontalface_default.xml')
font = cv2.FONT_HERSHEY_SIMPLEX
#iniciate id counter
id = 0
# names related to ids: example ==> Marcelo: id=1,  etc
names = ['host', 'tester1', 'tester2'] 
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # convert frame to array
    image = frame.array
    #Convert to grayscale
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    #Look for faces in the image using the loaded cascade file
    faces = face_cascade.detectMultiScale(gray, scaleFactor = 1.2, minNeighbors = 5, minSize = (100, 100), flags = cv2.CASCADE_SCALE_IMAGE)
    if (len(faces) == 0):
        lock()
    print ("Found "+str(len(faces))+" face(s)")
    #Draw a rectangle around every found face
    for (x,y,w,h) in faces:
        roi_gray = gray[y:y + h, x:x + w]
        cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
        # Check if confidence is less them 100 ==> "0" is perfect match 
        if (confidence > 0 and confidence < 60):
            id = "clear and try again"
            confidence = "  {0}%".format(round(confidence))
            lock()
        elif (confidence >= 60 and confidence <= 100):
            id = names[id]
            confidence = "  {0}%".format(round(confidence))
            unlock()
            time.sleep(1)
            lock()
        else:
            id = "unknown"
            confidence = "  {0}%".format(round(confidence))
            lock()
        
        cv2.putText(image, str(id), (x+5,y-5), font, 1, (0,0,255), 2)
        cv2.putText(image, str(confidence), (x+10,y+h-5), font, 1, (255,255,0), 1)  
        print(x,y,w,h)
    # display a frame
    #image = cv2.flip(image, 1)
    cv2.imshow("Frame", image)
    if cv2.waitKey(1) & 0xff == ord("q"):
	    exit()
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)