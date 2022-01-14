#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseStamped, Twist
import tf

# Déclaration de la variable globale goal
goal= PoseStamped()

# Subscriber node qui reçoit les informations d'objectifs de deplacement
def callback(data):
    global goal
    goal= data
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data)

# Second callback activé fréquemment, pour envoyer la commande de vélocité au robot
def move_command(data):
    goal.header.stamp= rospy.Time() #on s'en fout du temps donc on l'initialise à 0
    local_goal= tfListener.transformPose("base_footprint", goal)
    cmd= Twist()
    cmd.linear.x= 0.1
    commandPublisher.publish(cmd)

###########################################################################
# First of all:
rospy.init_node('talker', anonymous=True)

# Initialize ROS Publisher node
commandPublisher= rospy.Publisher('my_command', Twist, queue_size=10)

# Initialize ROS Subcriber node
rospy.Subscriber("goal", PoseStamped, callback)

# Initialisation de la variable globale qui subscribe aux topics tf
tfListener= tf.TransformListener()

# call the move_command at a regular frequency:
rospy.Timer( rospy.Duration(0.1), move_command, oneshot=False )

# spin() enter the program in a infinite loop
rospy.spin()

