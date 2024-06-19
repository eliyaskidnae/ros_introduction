#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from math import pi 

if __name__ == '__main__':
    rospy.init_node('draw_circle')
    rospy.loginfo("Draw circle node has benn started")
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)

    # r = rospy.Rate(100) # 10hz
    radius = 2
    while not rospy.is_shutdown():
        print("hello")
        msg = Twist()
        msg.linear.x = radius
        msg.angular.z = 2
        pub.publish(msg)
        rospy.sleep(1)
