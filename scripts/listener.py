#!/usr/bin/env python3
import rospy
from  std_msgs.msg import String
def sub_callback(res):

    rospy.loginfo(res.data)

if __name__ == '__main__':

    rospy.init_node("subscriber")
    rospy.loginfo("This Message subscriper  Node ")

    rospy.Subscriber('chatter' , String ,sub_callback)
    rospy.spin()