#!/usr/bin/env python3
from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray
from geometry_msgs.msg import Vector3
import rospy
import time



class Cube():
   def __init__(self):
      #date = time.process_time()
      #print(date)
      #rospy.init_node('marqueur')
      topic = 'visualization_marker'
      self.publisher = rospy.Publisher(topic, Marker, queue_size=10)

      # Initialisation du marker
      self.marker = Marker()
      self.marker.header.frame_id = "map"
      self.marker.type = Marker.CUBE
      self.marker.action = Marker.ADD

      # Cube de couleur verte
      self.marker.color.r = 0.0
      self.marker.color.g = 1.0
      self.marker.color.b = 0.0
      self.marker.color.a = 1.0

      # Scale du marker
      self.marker.scale.x = 0.2
      self.marker.scale.y = 0.2
      self.marker.scale.z = 0.2


   def pose(self, pos_x, pos_y, pos_z =0, or_x = 0, or_y = 0, or_z = 0, or_w= 0):
   # Pose du marker
      self.marker.pose.position.x = pos_x
      self.marker.pose.position.y = pos_y
      self.marker.pose.position.z = pos_z
      self.marker.pose.orientation.x = or_x
      self.marker.pose.orientation.y = or_y
      self.marker.pose.orientation.z = or_z
      self.marker.pose.orientation.w = or_w

   def publishing(self):
         self.publisher.publish(self.marker)
         #rospy.rostime.wallsleep(1.0)


if __name__ == '__main__':
   cube1 = Cube()
   cube1.pose(0, 3)
   cube1.publish()
   
