#!/usr/bin/python3
import math, rospy, math
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import time
import random

# Initialize variables
collision = False
marche_avant = True
tirage = 0

# robot variable 
STEP_X = 2
STEP_Z = 1

# Initialize ROS::node
rospy.init_node('move', anonymous=True)

commandPublisher = rospy.Publisher(
    '/cmd_vel_mux/input/navi',
    Twist, queue_size=10
)

# Publish velocity commandes:
def move_command(data):
    # Compute cmd_vel here and publish... (do not forget to reduce timer duration)
    global marche_avant, tirage
    if collision == False:  #si pas de collisions alors le robot avance
        marche_avant = True
        cmd= Twist()
        cmd.linear.x= STEP_X
        commandPublisher.publish(cmd)
    else:   #si collision alors le robot tourne
        cmd = Twist()
        print('tirage = ' + str(tirage))
        if marche_avant == True: 
            tirage = random.randint(0, 1)
            print('tirage = ' + str(tirage))
            marche_avant = False
        if tirage == 0:
            cmd.angular.z = STEP_Z #GAUCHE
        else:
            cmd.angular.z = -STEP_Z  #DROITE
        commandPublisher.publish(cmd)
        time.sleep(1)

def interpret_scan(data):
    #interpètre les données
    global collision #déclaration variable globale 
    #rospy.loginfo('I get scans')
    obstacles= []
    angle= data.angle_min
    for aDistance in data.ranges :
        if 0.1 < aDistance and aDistance < 5.0 :
            aPoint= [ 
                math.cos(angle) * aDistance, 
                math.sin( angle ) * aDistance
            ]
            obstacles.append( aPoint )
        angle+= data.angle_increment
    #rospy.loginfo( str(
    #    [ [ round(p[0], 2), round(p[1], 2) ] for p in  obstacles[0:10] ] 
    #) + " ..." )
    collision = amIcollision(obstacles)

def amIcollision(obstacles):
    #test si le robot est en collisions
    for p in obstacles:     #test toutes les valeurs du dico obstacles
        if abs(p[0]) <= 0.7 and abs(p[0]) >= 0.05:     #test l'axe des x à 20 cm
            #print('x =' + str(p[0]) + 'y =' + str(p[1]))
            #time.sleep(0.5)
            if p[1] <= 0.2 and p[1] >= -0.2: #test l'axe des y pour une ouverture de 90°
                return True
    return False

# connect to the topic:
rospy.Subscriber('scan', LaserScan, interpret_scan)

# Boucle programme 
rospy.Timer(rospy.Duration(0.1), move_command, oneshot=False)

rospy.spin()