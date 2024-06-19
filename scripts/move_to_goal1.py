
#!/usr/bin/env python3

import rospy
from  std_msgs.msg import String
from  geometry_msgs.msg import Twist
from  turtlesim.msg import Pose
from math import atan2 , sqrt , degrees , radians , pi , floor
import sys
import time
from  nav_msgs.msg import Odometry
import tf 

def wrap_angle(angle):
    # warap angle
    
    return (angle + (2*3.14*floor((3.14 - angle)/(2*3.14))))
    

class Move() : 

    def __init__(self , target_x, target_y):
        # # all initilizations g
        self.tolorance = 0.1
        self.Kh = 5
        self.Kv = 2

        self.target_x = target_x
        self.target_y = target_y

        rospy.init_node('move_to_pose', anonymous=True)
        # publisher
        self.vel_pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
        # subscriper
        self.pose_sub = rospy.Subscriber('/turtle1/pose',Pose,self.callback)  

        self.pose = Pose()
        self.vel_msg = Twist()

    def callback(self,req): 
        # the current pose and orientation of the turtle
        pose = Pose()
        # # print(req)
        pose = req
        self.pose.x = pose.x
        self.pose.y = pose.y
        self.pose.theta = pose.theta

    def distance_to_goal(self):
        return sqrt((self.target_x-self.pose.x)**2 +(self.target_y-self.pose.y)**2)
    


    def move_to_goal(self):
        time.sleep(0.1)
        print(self.pose.x , self.pose.y ,self.distance_to_goal() , self.tolorance )


        while(self.distance_to_goal() > self.tolorance ):
            # print(self.pose.x , self.pose.y)
            d = self.distance_to_goal()
            psi_d = atan2(self.target_y - self.pose.y, self.target_x - self.pose.x)
            w_d = self.Kh*wrap_angle(psi_d-self.pose.theta)
            v_d = self.Kv*d
        
            self.vel_msg.linear.x = v_d
            self.vel_msg.angular.z = w_d
            self.vel_pub.publish(self.vel_msg)
            # time.sleep(0.1)

        self.vel_msg.linear.x = 0
        self.vel_msg.angular.z = 0
        self.vel_pub.publish(self.vel_msg)

    def set_goal(self ,target_x , target_y ):
        
        self.target_x = target_x
        self.target_y = target_y

      

if __name__ == '__main__':
    
    try:
       
       target_x = 1
       target_y = 1
       if(len(sys.argv) > 1):
            target_x = float(sys.argv[1])
            target_y = float(sys.argv[2])

       else:
           target_x = rospy.get_param("target_x")
           target_y = rospy.get_param("target_y")

       print(target_x, target_y)
       
       move = Move(target_x , target_y)
       move.move_to_goal()
       
    #    move.set_goal(target_x , target_y)
       rospy.spin()
       
    except rospy.ROSInterruptException: pass
   
