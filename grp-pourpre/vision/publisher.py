#!/usr/bin/env python

#import de classe
import rospy
from visualization_msgs.msg import Marker

#création classe
class Bottle:
    def __init__(self):
        # constructeur 
        self.topic = 'visualization_marker'
        self.publisher = rospy.Publisher(self.topic, Marker)
        rospy.init_node('bottle')

    def run(self):
        # programme qui va tourner lors du fonctionnement 
        while not rospy.is_shutdown():

