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

# test segmentation image 
# from sklearn.cluster import KMeans
# import matplotlib.pyplot as plt

# def seg(image):
#     #segmente l'Image()
#     n_clusters= 3
#     image = image.reshape((image.shape[0] * image.shape[1], 3))
#     clt = KMeans(n_clusters = n_clusters )
#     clt.fit(image)

# def centroid_histogram(clt):
#     #numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)>>>
#     (hist, _) = np.histogram(clt.labels_, bins=numLabels)

#     # normalize the histogram, such that it sums to one
#     hist = hist.astype("float")
#     hist /= hist.sum()

#     return hist

# def plot_colors(hist, centroids):
#     bar = np.zeros((50, 300, 3), dtype="uint8")
#     startX = 0

#     # loop over the percentage of each cluster and the color of
#     # each cluster
#     for (percent, color) in zip(hist, centroids):
#         # plot the relative percentage of each cluster
#         endX = startX + (percent * 300)
#         cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
#                       color.astype("uint8").tolist(), -1)
#         startX = endX

#     return bar

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
coord_detection = None
global_pose = PoseStamped()

def callback(data):
    global cv_image
    try:
        print("callback")
        cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
        detection()
    except CvBridgeError as e:
        print(e)
  
def robotPosition():
    pose= PoseStamped()
    pose.header.frame_id= "base_link"
    global_pose= tfListener.transformPose("map", pose)
    return global_pose

def pose_cube():
    cube = Cube()
    coord = robotPosition()
    cube.pose(coord.pose.position.x, coord.pose.position.y)
    cube.publishing()

def detection():
    global cam, cv_image
    print("detection function")
    # programme de détection 
    # Capture the video frame-by-frame
    if type(cv_image) != None: #si image non initialisé 
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        print("dans if type detection")


        # You must enter the values for the parameters denoted with callbackan x
        #gray = np.array(gray, dtype='uint8')

        lo = 240
        hi = 255
        mask=cv2.inRange(gray, lo, hi) # fonction qui filtre en blanc tous leCascade.detectMultiScale(image = gray, scaleFactor = 1.05, minNeighbors = 4, minSize=(30,30), maxSize=(70, 70)) xels de la zone blanche 
        image2=cv2.bitwise_and(cv_image, cv_image, mask= mask) # permets d'afficher l'image segmenté avec un et logique 
        #gray = image2
        faces = faceCascade.detectMultiScale(image = gray, scaleFactor = 1.05, minNeighbors = 100, minSize=(15,30), maxSize=(70, 70))
        
        # Drawing rectangle around the face
        for (x, y, w, h) in faces:
            cv2.rectangle(cv_image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            #if faces is not None:
            print("appel pose cub")
            pose_cube()
                
        # Show the frame
        print("> The show go on")
        cv2.imshow('Video', cv_image)
        cv2.imshow('video2', image2)

    print("> detection end")

def callback2(data):
    i = 1 



#initalisation node
rospy.init_node('Vision_Node', anonymous=True)  

tfListener = tf.TransformListener()
rospy.Subscriber("camera/color/image_raw", Image, callback) #connection subscriber
rospy.Subscriber("camera/depth/image_rect_raw", Image, callback2)
#rospy.Timer(rospy.Duration(0.1), detection) # lance le programme de détection rate 10 Hz
rospy.spin() #boucle infinie