#!/usr/bin/env python
"""Raspberry Pi Face Recognition Treasure Box
Treasure Box Script
Copyright 2013 Tony DiCola 
Copyright 2016 Monsieur Vechai
"""
import cv2
import config, face
import time
camera = cv2.VideoCapture(config.WEBCAM_ID)

if __name__ == '__main__':
	# Load training data into model
	print 'Loading training data...'
	model = cv2.createEigenFaceRecognizer()
	model.load(config.TRAINING_FILE)
	print 'Training data loaded!'
        time_end = time.time() + 60 * 15
        while time.time() < time_end:
            # Initialize camer and box.'	
            ret1, frame1 = camera.read()
            image = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
            result = face.detect_single(image)
            if result is None:
                print 'Could not detect single face!'
            else:
                x, y, w, h = result
                crop = face.resize(face.crop(image, x, y, w, h))
                label, confidence = model.predict(crop)
                print 'Predicted {0} face with confidence {1} (lower is more confident).'.format(
           					'POSITIVE' if label == config.POSITIVE_LABEL else 'NEGATIVE', 
           					confidence)
           	if label == config.POSITIVE_LABEL and confidence < config.POSITIVE_THRESHOLD:
           	    print 'Recognized face!'
           	else:
           	    print 'Did not recognize face!'
	   
        camera.release()
        cv2.destroyAllWindows()
	