import cv2
import sys
import numpy as np

#cascPath = '/home/pierrick/catkin_ws/src/opencv-haar-classifier-training/data/cascade.xml'
cascPath = '/home/pierrick/data_old/cascade.xml'
faceCascade = cv2.CascadeClassifier(cascPath)
print(cv2.data.haarcascades)

#faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + '/cascade.xml')

def isIempty(face):
    # fonction qui sert à détecter si un objet est détecté 
    if len(face) == 0:
        print("rien n'est détecté")
        return False
    else:
        print("une bouteille est détectée")
        return True 

#video_capture = cv2.VideoCapture(0)

# Subscriber node afin de recevoir les messages de la caméra
def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    
def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("camera/color/image_raw", Image, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()



while True:
# Capture the video frame-by-frame
    ret, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# You must enter the values for the parameters denoted with an x
    gray = np.array(gray, dtype='uint8')
    faces = faceCascade.detectMultiScale(gray, 3, 2, 0)
    #isIempty(faces)
    print(faces)

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