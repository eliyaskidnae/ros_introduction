
#!/usr/bin/env python3
import rospy
from turtlesim.msg import Pose
def Publish_Pose(msg):
    rospy.loginfo(msg)

if __name__ == '__main__':

    rospy.init_node("Subscriper Node")
    rospy.loginfo(" Subscriper Node Started ")
    
    rospy.Subscriber('turtle1/pose',Pose,callback= Publish_Pose )

    rospy.spin()


