#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
def logger():
   
   rospy.init_node('This Log File', anonymous=True , log_level=rospy.FATAL)
   rate = rospy.Rate(10) # 10hz
   while not rospy.is_shutdown():
        
        hello_str = "hello world %s" % rospy.get_time()
        rospy.loginfo(hello_str)
        rospy.logdebug("This is a debug message.")
        rospy.logwarn("Battery level is low.")
        rospy.logerr("Failed to execute motion plan.")
        rospy.logfatal("Critical hardware failure detected. Shutting down.")

        rate.sleep()
  
if __name__ == '__main__':
      try:
          logger()
      except rospy.ROSInterruptException:
           pass