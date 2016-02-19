#!/usr/bin/python2
import sys
import cv2
import numpy

# Get user supplied values
cascPath = sys.argv[1]

# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascPath)

# Read the image
video_capture = cv2.VideoCapture(0)
ret, image = video_capture.read()
#gray = cv2.cvtColor(image, cv2.CV_BGR2GRAY)
gray = image

# Detect faces in the image
faces = faceCascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(30, 30),
    flags = cv2.CASCADE_SCALE_IMAGE
)

# Draw a rectangle around the faces
for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x+w, y+h), (255, 36, 36), 5)

cv2.imwrite("processed_shot.png", image)



cv2.waitKey(0)
