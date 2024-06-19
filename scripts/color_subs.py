
#!/usr/bin/env python3
import rospy
from turtlesim.msg import Color

def get_color(msg):
    rospy.loginfo(msg)

if __name__ == '__main__':

    rospy.init_node("color_sub")
    rospy.loginfo(" Subscriper Node Started ")
    
    rospy.Subscriber('turtle1/color_sensor',Color,callback= get_color )

    rospy.spin()


