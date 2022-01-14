import cv2
import sys
import numpy as np
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import tf
from geometry_msgs.msg import PoseStamped, Twist

#cascPath = '/home/pierrick/catkin_ws/src/opencv-haar-classifier-training/data/cascade.xml'  #machine pipi
#cascPath = '/home/pierrick/data_old/cascade.xml' #machine pipi
cascPath = '/home/pierrick.bougault/Bureau/cascade.xml'  #poste école
faceCascade = cv2.CascadeClassifier(cascPath)
#print(cv2.data.haarcascades)

#faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + '/cascade.xml')

# fonction qui sert à détecter si un objet est détecté 
def isIempty(face):
    if len(face) == 0:
        print("rien n'est détecté")
        return False
    else:
        print("une bouteille est détectée")
        return True 

# Subscriber node afin de recevoir les messages de la caméra
# Initialisation de la variable globale
cam = Image()
bridge = CvBridge()
cv_image = None
coord_detection = None
global_pose = PoseStamped()

def callback(data):
    global cam, cv_image
    cam= data
    #rospy.loginfo(rospy.get_caller_id() + "I heard %s", cam)
    try:
        cv_image = bridge.imgmsg_to_cv2(cam, "bgr8")
        #print("cv image callback =" + cv_image)
    except CvBridgeError as e:
        print(e)
    #print( type(cv_image) ) debug 

def detection(self):
    # programme de détection 
    # Capture the video frame-by-frame
    if type(cv_image) != None: #si image non initialisé 
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

        # You must enter the values for the parameters denoted with callbackan x
        gray = np.array(gray, dtype='uint8')
        faces = faceCascade.detectMultiScale(gray, 1, 3, 0)
        #isIempty(faces)
        
        # Drawing rectangle around the face
        for (x, y, w, h) in faces:
            cv2.rectangle(cv_image, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Show the frame
        cv2.imshow('Video', cv_image)

        # Quit the program with the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            breaklistener=()

def callback2(data):
    #
    i = 1 


def robotPosition():
    pose= PoseStamped()
    pose.header.frame_id= "base_link"
    global_pose= tfListener.transformPose("map", pose)
    return  global_pose

#initalisation ode
rospy.init_node('python', anonymous=True)  

tfListener = tf.TransformListener()
rospy.Subscriber("camera/color/image_raw", Image, callback) #connection subscriber
rospy.Subscriber("camera/depth/image_rect_raw", Image, callback2)
rospy.Timer(rospy.Duration(0.1), detection) # lance le programme de détection rate 10 Hz

rospy.spin() #boucle infini