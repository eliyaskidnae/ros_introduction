#!usr/bin/env/ python3 
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import SetPen

pre_pose = 5
def call_set_pen_Service(r,b,g,width,off):

    try:
        setpen = rospy.ServiceProxy("turtle1/set_pen",SetPen)
        res    = setpen(r,b,g,width,off)
        
    except rospy.ServiceException as e:
        rospy.logwarn(e)
    
        
def publish_controller(pose:Pose):
    
  
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    cmd = Twist()
    if(2 > pose.x or pose.x > 9 or 2 >pose.y or pose.y>9):
        cmd.linear.x = 1
        cmd.angular.z = 1.4
    else:
        cmd.linear.x =5
        cmd.angular.z = 0 # straight line move 
        print(pose)

    pub.publish(cmd)
    global pre_pose
    if(pose.x>5 and pre_pose<5):
        call_set_pen_Service(0,255,0,3,0)
    elif(pose.x<5 and pre_pose>5):
        call_set_pen_Service(255,0,0,3,0)
    pre_pose = pose.x
if __name__ == '__main__':
    rospy.init_node('turtle_controller')
    rospy.wait_for_service("turtle1/set_pen")
    
    rospy.loginfo("Draw circle node has benn started")

    sub = rospy.Subscriber('/turtle1/pose',Pose,publish_controller)
    rospy.spin()