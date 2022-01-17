#!/usr/bin/env python3

import cv2
import sys
import numpy as np
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import tf
from geometry_msgs.msg import PoseStamped, Twist, Point, Pose
from visualization_msgs.msg import Marker
import rospkg 
rospack= rospkg.RosPack()
sys.path.append( rospack.get_path('grp-pourpre') + "/scripts" )
from mymarker import Cube

#cascPath = '/home/pierrick/catkin_ws/src/opencv-haar-classifier-training/data/cascade.xml'  #machine pipi
#cascPath = '/home/pierrick/data_old/cascade.xml' #machine pipi
cascPath = '/home/pierrick.bougault/Bureau/cascade.xml'  #poste école
faceCascade = cv2.CascadeClassifier(cascPath)
#print(cv2.data.haarcascades)

#faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + '/cascade.xml')

# Subscriber node afin de recevoir les messages de la caméra
# Initialisation de la variable globale
bridge = CvBridge()
cv_image = None
cv_depth = None
coord_detection = None
global_pose = PoseStamped()
face_width = 0
abscisse = 0
ordonnee = 0

def callback(data):
    global cv_image
    try:
        # print("callback")
        cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
        detection()
    except CvBridgeError as e:
        print(e)
  
def robotPosition():
    pose= PoseStamped()
    pose.header.frame_id= "base_link"
    global_pose= tfListener.transformPose("map", pose)
    return global_pose

def pose_cube(x, y):
    cube = Cube()
    #coord = robotPosition()
    cube.pose(x,y)
    cube.publishing()
    #print("x , y =" + str(x) + '\n' + str(y))

def detection():
    global cam, cv_image, face_width, abscisse
    # programme de détection 
    # Capture the video frame-by-frame
    if type(cv_image) != None: #si image non initialisé 
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        # You must enter the values for the parameters denoted with callbackan x
        #gray = np.array(gray, dtype='uint8')

        lo = 240
        hi = 255
        mask=cv2.inRange(gray, lo, hi) # fonction qui filtre en blanc tous leCascade.detectMultiScale(image = gray, scaleFactor = 1.05, minNeighbors = 4, minSize=(30,30), maxSize=(70, 70)) xels de la zone blanche 
        image2=cv2.bitwise_and(cv_image, cv_image, mask= mask) # permets d'afficher l'image segmenté avec un et logique 
        #gray = image2
        faces = faceCascade.detectMultiScale(image = gray, scaleFactor = 1.05, minNeighbors = 200, minSize=(15,30), maxSize=(70, 70))
        
        # Drawing rectangle around the face
        for (x, y, w, h) in faces:
            cv2.rectangle(cv_image, (x, y), (x+w, y+h), (255, 255, 0), 2)

            #if faces is not None:
            #pose_cube()
            face_width = w # argument fonction z
            #if ( x + (w/2) < 720):
            print("tetete")
            profondeur = cv_depth[int( y+(h/2)   ),int( x+(w/2))]
            cv2.rectangle(cv_image, ( int(y+(h/2) ),int(x+(w/2)),(int(y+(h/2)+10),int(x+(w/2)+10)) ,(0,0,255))) 
            print('prof =' + str(profondeur))
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(cv_image, str(profondeur) + ' mm',(x,y), font, .5, (255,255,0), 2, cv2.LINE_AA)
            #print("coordonée abscisse =" + str(abscisse))
            # pose_robot = robotPosition()
            # ordonnee = x/500 + pose_robot.pose.position.y
            # abscisse = pose_robot.pose.position.x + Distance_finder(x+w) 
            # #+ pose_robot.pose.position.x
            # pose_cube(ordonnee = 0, abscisse)
            #print("pose robot : " + str(pose_robot))

                
        # Show the frame
        cv2.imshow('Video', cv_image)
        cv2.waitKey(3)

def FocalLength(measured_distance = 45, real_width = 5.5): 
    # variable de référence mesuré à la main 
    # measured_distance : distance de la position de référence
    # real_with : largeur réelle de la bouteille 
    focal_length = (face_width* measured_distance)/ real_width
    return focal_length

def Distance_finder(face_width_in_frame, real_bottle_width = 5.5):
    focal_length = FocalLength()
    distance = (real_bottle_width * focal_length)/face_width_in_frame
    return distance

def callback2(data):
    global cv_depth
    try:
        # print("callback")
        cv_depth = bridge.imgmsg_to_cv2(data, "passthrough")
        cv2.imshow('video_depth', cv_depth)
        cv2.waitKey(3)
    except CvBridgeError as e:
        print(e)

#initalisation node
rospy.init_node('Vision_Node', anonymous=True)  

tfListener = tf.TransformListener()
rospy.Subscriber("/camera/color/image_raw", Image, callback) #connection subscriber
rospy.Subscriber("camera/aligned_depth_to_color/image_raw", Image, callback2)
#rospy.Timer(rospy.Duration(0.1), detection) # lance le programme de détection rate 10 Hz
rospy.spin() #boucle infinie