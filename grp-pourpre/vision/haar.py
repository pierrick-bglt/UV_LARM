import cv2
import sys
import numpy as np

cascPath = 'haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)

while True:
# Capture the video frame-by-frame
    ret, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# You must enter the values for the parameters denoted with an x
    gray = np.array(gray, dtype='uint8')
    faces = faceCascade.detectMultiScale(gray, 1.3, 2, 0)

# Drawing rectangle around the face
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

# Show the frame
    cv2.imshow('Video', frame)

# Quit the program with the 'q' key is pressed

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture when program terminates
video_capture.release()
cv2.destroyAllWindows()