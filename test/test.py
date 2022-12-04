import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)
GPIO.output(26, 1)
time.sleep(2)
GPIO.output(26, 0)
GPIO.cleanup()
