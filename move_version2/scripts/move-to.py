#!/usr/bin/python3
import math, rospy
from geometry_msgs.msg import PoseStamped
import tf


class TurtleBot:

    def __init__(self):
            # Creates a node with name 'turtlebot_controller' and make sure it is a
            # unique node (using anonymous=True).
            rospy.init_node('goal', anonymous=True)

            # Publisher which will publish to the topic '/turtle1/cmd_vel'.
            self.velocity_publisher = rospy.Publisher('/cmd_vel', PoseStamped(), queue_size=10)

            # A subscriber to the topic '/turtle1/pose'. self.update_pose is called
            # when a message of type Pose is received.
            self.pose_subscriber = rospy.Subscriber('/base_link_in_odom', PoseStamped, self.update_pose)

            #self.pose = Pose()
            self.rate = rospy.Rate(10)

    def update_pose(self, data):
        # coordonnée non transformé base odom
        self.pose = data
        self.pose.x = round(self.pose.x, 4)
        self.pose.y = round(self.pose.y, 4)
        self.pose.z = round(self.pose.z, 4)

    def transform_coord(self):
        # transforme les coordonées de la base odom en base footprint

        



    # def euclidean_distance(self, goal_pose):
    #     """Euclidean distance between current pose and the goal."""
    #     return sqrt(pow((goal_pose.x - self.pose.x), 2) +
    #                 pow((goal_pose.y - self.pose.y), 2))

    # def linear_vel(self, goal_pose, constant=1.5):
    #     """See video: https://www.youtube.com/watch?v=Qh15Nol5htM."""
    #     return constant * self.euclidean_distance(goal_pose)

    # def steering_angle(self, goal_pose):
    #     """See video: https://www.youtube.com/watch?v=Qh15Nol5htM."""
    #     return atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x)

    # def angular_vel(self, goal_pose, constant=6):
    #     """See video: https://www.youtube.com/watch?v=Qh15Nol5htM."""
    #     return constant * (self.steering_angle(goal_pose) - self.pose.theta)

    def move2goal(self):
        """Moves the turtle to the goal."""
        goal_pose = PoseStamped()

        # Get the input from the user.
        goal_pose.x = float(input("Set your x goal: "))
        goal_pose.y = float(input("Set your y goal: "))

        # Please, insert a number slightly greater than 0 (e.g. 0.01).
        distance_tolerance = input("Set your tolerance: ")

        vel_msg = Twist()

        while self.euclidean_distance(goal_pose) >= distance_tolerance:

            # Porportional controller.
            # https://en.wikipedia.org/wiki/Proportional_control

            # Linear velocity in the x-axis.
            vel_msg.linear.x = self.linear_vel(goal_pose)
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0

            # Angular velocity in the z-axis.
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z = self.angular_vel(goal_pose)

            # Publishing our vel_msg
            self.velocity_publisher.publish(vel_msg)

            # Publish at the desired rate.
            self.rate.sleep()

        # Stopping our robot after the movement is over.
        vel_msg.linear.x = 0
        vel_msg.angular.z = 0
        self.velocity_publisher.publish(vel_msg)

        # If we press control + C, the node will stop.
        rospy.spin()

if __name__ == '__main__':
    try:
        x = TurtleBot()
        x.move2goal()
    except rospy.ROSInterruptException:
        pass

#     # Initialize ROS::node
#     pub = rospy.Publisher('chatter', PoseStamped, queue_size=10)
#     rospy.init_node('move2', anonymous=True)
#     #rate = rospy.Rate(10) # 10hz
#     commandPublisher = rospy.Publisher(
#         '/cmd_vel',
#         PoseStamped, queue_size=10
#     )

# def callback(data):
# 	print("info : %s", data.pose.pose)


# # Publish velocity commandes:
# def move_command(data):
#     # Compute cmd_vel here and publish... (do not forget to reduce timer duration)
#     cmd= PoseStamped()
#     cmd.linear.x= 0.1
#     commandPublisher.publish(cmd)

# # call the move_command at a regular frequency:
# #rospy.Timer( rospy.Duration(0.1), move_command, oneshot=False )

# # spin() enter the program in a infinite loop
# print("Start move.py")
# # connect to the topic:
# rospy.init_node('/base_link_in_odom', anonymous=True)
# rospy.Subscriber('goal', PoseStamped(), callback)
# rospy.spin()
