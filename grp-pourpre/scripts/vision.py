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
from visualization_msgs.msg import MarkerArray
import rospkg 
from math import sqrt
# rospack= rospkg.RosPack()
# sys.path.append( rospack.get_path('grp-pourpre') + "/scripts" )
# from mymarker import Cube

#cascPath = '/home/pierrick/catkin_ws/src/opencv-haar-classifier-training/data/cascade.xml'  #machine pipi
cascPath = '/home/pierrick/data_old/cascade.xml' #machine pipi
#cascPath = '/home/pierrick.bougault/Bureau/cascade.xml'  #poste école
#cascPath = '/home/pierrick/catkin_ws/src/UV_LARM/grp-pourpre/scripts/cascade.xml'
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

class Cube():
    lastSeq = -1
    marker_array_msg = MarkerArray()
    marker_log = []

    def __init__(self, pos_x, pos_y, pos_z =0, or_x = 0, or_y = 0, or_z = 0, or_w= 0):
        topic = '/visualization_marker_array'
        #rospy.init_node(topic, anonymous=True)  
        self.publisher = rospy.Publisher(topic, MarkerArray, queue_size=10)
        self.tfListener= tf.TransformListener()
        self.i = 0
        # # Initialisation du marker
        self.lastBottle = Marker()
        self.lastBottle.header.frame_id = "base_footprint"
        self.lastBottle.header.stamp = rospy.Time.now()
        self.lastBottle.type = Marker.CUBE
        self.lastBottle.action = Marker.ADD
        # CublastBottleouleur verte
        self.lastBottle.color.r = 0.0
        self.lastBottle.color.g = 1.0
        self.lastBottle.color.b = 0.0
        self.lastBottle.color.a = 1.0
         # ScalastBottlemarker
        self.lastBottle.scale.x = 0.2
        self.lastBottle.scale.y = 0.2
        self.lastBottle.scale.z = 0.2
        self.lastBottle.lifetime = rospy.Duration(0)
        # initialisation id marker 
        Cube.lastSeq = Cube.lastSeq + 1
        self.lastBottle.id = Cube.lastSeq
        # affectation coordonnées 
        self.lastBottle.pose.position.x = pos_x / 1000
        self.lastBottle.pose.position.y = pos_y / 1000
        self.lastBottle.pose.position.z = pos_z
        self.lastBottle.pose.orientation.x = or_x
        self.lastBottle.pose.orientation.y = or_y
        self.lastBottle.pose.orientation.z = or_z
        self.lastBottle.pose.orientation.w = or_w

        self.publish = self.transformation()
        if self.publish == True:
            self.publishing()
            
    def distance(self, xa, xb, ya, yb):
        return sqrt(  (xb - xa)**2 + (yb - ya)**2  )

    def get_minimal_dist(self):
        #if len(self.marker_log) > 1:
            min_dist = self.distance(Cube.marker_log[0][0], self.lastBottle.pose.position.x, Cube.marker_log[0][1], self.lastBottle.pose.position.y)
            for i in range(len(self.marker_log)):
                dist = self.distance(Cube.marker_log[i][0], self.lastBottle.pose.position.x, Cube.marker_log[i][1], self.lastBottle.pose.position.y)
                if (dist<min_dist) :
                    min_dist = dist
                    #print(min_dist)                
            return min_dist
    
    def transformation(self):
        # transforme les coordonées robot vers map 
        bottlePoseStamped= PoseStamped()
        bottlePoseStamped.header = self.lastBottle.header
        bottlePoseStamped.header.frame_id= self.lastBottle.header.frame_id
        bottlePoseStamped.pose = self.lastBottle.pose    # conversion de bottleposition en posestamped
        bottleTransformed = self.tfListener.transformPose("base_footprint", bottlePoseStamped)
        self.lastBottle.header = bottleTransformed.header
        self.lastBottle.pose = bottleTransformed.pose
        if len(Cube.marker_log) > 0:
            if self.get_minimal_dist() >= 0.4:
                Cube.marker_log.append((self.lastBottle.pose.position.x, self.lastBottle.pose.position.y))
                Cube.marker_array_msg.markers.append(self.lastBottle)
                return True 
            else:
                return False
        else:
            Cube.marker_log.append((self.lastBottle.pose.position.x, self.lastBottle.pose.position.y))
            return True 

    def publishing(self):
       #publie la liste de marqueur
        self.publisher.publish(Cube.marker_array_msg)
        self.publish = False


def callback(data):
    global cv_image
    try:
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

def red_detection(cv_image):
    # define the list of boundaries
    boundaries = [([0, 190, 190], [25,255,255]), #rouge
    ([0, 0, 180], [255, 255, 255]), #blanc
    ([0,0,0], [90,90,90]) #noir
    ]
    # loop over the boundaries
    for (lower, upper) in boundaries:
        # create NumPy arrays from the boundaries
        hsv_px = cv2.cvtColor(cv_image,cv2.COLOR_BGR2HSV)
        lower = np.array(lower, dtype = "uint8")
        upper = np.array(upper, dtype = "uint8")
        # find the colors within the specified boundaries and apply
        # the mask
        mask = cv2.inRange(hsv_px, lower, upper)
        output = cv2.bitwise_and(cv_image, cv_image, mask = mask)
        # show the images
        cv2.imshow("red", output)
        cv2.waitKey(3)

def detection():
    # programme de détection de bouteille
    global cam, cv_image, face_width, abscisse
    # Capture the video frame-by-framebottlePosition
    if type(cv_image) != None: #si image non initialisé 
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        # You must enter the values for the parameters denoted with callbackan x
        #gray = np.array(gray, dtype='uint8')
        faces = faceCascade.detectMultiScale(image = gray, scaleFactor = 1.05, minNeighbors = 200, minSize=(15,30), maxSize=(70, 70))
        # Drawing rectangle around the face
        for (x, y, w, h) in faces:
            cv2.rectangle(cv_image, (x, y), (x+w, y+h), (255, 255, 0), 2)
            face_width = w # argument fonction z
            if ( y+(h/2) < 720):
                profondeur = cv_depth[int( y+(h/2)   ),int( x+(w/2))]
                cv2.rectangle(cv_image, ( int( x+(w/2)  ),int( y+(h/2)  )),(int( x+(w/2) +10 ),int(  y+(h/2)  +10)) ,(0,0,255)) 
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(cv_image, str(profondeur) + ' mm',(x,y), font, .5, (255,255,0), 2, cv2.LINE_AA)
                Cube(profondeur, y)
                red_detection(cv_image)              
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
        cv_depth = bridge.imgmsg_to_cv2(data, "passthrough")
        #cv2.imshow('video_depth', cv_depth)
        #cv2.waitKey(3)
    except CvBridgeError as e:
        print(e)

#initalisation node
rospy.init_node('Vision_Node', anonymous=True)  

tfListener = tf.TransformListener()
rospy.Subscriber("/camera/color/image_raw", Image, callback) #connection subscriber
rospy.Subscriber("camera/aligned_depth_to_color/image_raw", Image, callback2)
#rospy.Timer(rospy.Duration(0.1), detection) # lance le programme de détection rate 10 Hz
rospy.spin() #boucle infinie