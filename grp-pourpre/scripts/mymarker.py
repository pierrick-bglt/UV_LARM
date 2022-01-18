#!/usr/bin/env python3

from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray
import rospy
from geometry_msgs.msg import PoseStamped
import tf

class Cube():
   def __init__(self):
      topic = '/visualization_marker'
      #rospy.init_node(topic, anonymous=True)  
      self.publisher = rospy.Publisher(topic, MarkerArray, queue_size=10)

      self.tfListener= tf.TransformListener()
      self.marker_array_msg = MarkerArray()
      self.i = 0

      # # Initialisation du marker
      self.marker = Marker()
      self.marker.header.frame_id = "map"
      self.marker.header.stamp = rospy.Time.now()
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


      # Scale du marker
      self.marker.scale.x = 0.2
      self.marker.scale.y = 0.2
      self.marker.scale.z = 0.2
      self.marker.lifetime = rospy.Duration(0)
      print('coord =' + str( self.marker.pose.position.x )  + '\n' + str( self.marker.pose.position.y))

      self.lastBottle  = None

   def pose(self, pos_x, pos_y, pos_z =0, or_x = 0, or_y = 0, or_z = 0, or_w= 0):
   # Pose du marker
      self.lastBottle.pose.position.x = pos_x / 1000
      self.lastBottle.pose.position.y = pos_y / 1000
      self.lastBottle.pose.position.z = pos_z
      self.lastBottle.pose.orientation.x = or_x
      self.lastBottle.pose.orientation.y = or_y
      self.lastBottle.pose.orientation.z = or_z
      self.lastBottle.pose.orientation.w = or_w
      self.marker_array_msg.markers.append(self.lastBottle) 


   def transformation(self):
      #print('x =' + str(self.marker.pose.position.x) + 'y =' + str(self.marker.pose.position.y))
      bottlePosition= Marker()
      bottlePosition.type = Marker.CUBE
      bottlePosition.action = Marker.ADD

      # Cube de couleur verte
      bottlePosition.color.r = 0.0
      bottlePosition.color.g = 1.0
      bottlePosition.color.b = 0.0
      bottlePosition.color.a = 1.0

      # Scale du marker
      bottlePosition.scale.x = 0.2
      bottlePosition.scale.y = 0.2
      bottlePosition.scale.z = 0.2

      bottlePoseStamped= PoseStamped()
      bottlePoseStamped.header = self.marker.header
      bottlePoseStamped.pose = self.marker.pose    # conversion de bottleposition en posestamped
      #print("bottleposestamped =" + str(bottlePoseStamped))
      bottleTransformed = self.tfListener.transformPose("map", bottlePoseStamped)
      bottlePosition.header = bottleTransformed.header
      bottlePosition.pose = bottleTransformed.pose

      bottlePosition.id = self.i
      self.i += 1

      self.lastBottle = bottlePosition
      
   def publishing(self):
      print(self.lastBottle)
      self.publisher.publish(self.marker_array_msg)

if __name__ == '__main__':
   cube1 = Cube()
   cube1.pose(0, 3)
   cube1.publishing()