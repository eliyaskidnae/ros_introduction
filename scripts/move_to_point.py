
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
    
    return (angle + (2*3.14*floor((3.14 -angle)/(2*3.14))))
    

class Move() : 

    def __init__(self):
        # # all initilizations g
        self.tolorance = 0.2
        self.Kh = 5
        self.Kv = 2
        rospy.init_node('move_to_pose', anonymous=True)
        # publisher
        self.vel_pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
        self.odom_pub = rospy.Publisher('/turtle1/odom', Odometry , queue_size=10)


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

        odom = Odometry()

        odom.header.stamp = rospy.Time.now()
        odom.header.frame_id = "map"

        odom.pose.pose.position.x = req.x
        odom.pose.pose.position.y = req.y
        odom.pose.pose.position.z = 0.0

        quaternion = tf.transformations.quaternion_from_euler(0,0,req.theta)
        
        odom.pose.pose.orientation.x = quaternion[0]
        odom.pose.pose.orientation.y = quaternion[1]
        odom.pose.pose.orientation.z = quaternion[2]
        odom.pose.pose.orientation.w = quaternion[3]

        odom.twist.twist.linear.x = req.linear_velocity
        odom.twist.twist.angular.y = req.angular_velocity

        # print(odom)
        self.odom_pub.publish(odom)

        # Timer
        self.timer = rospy.Timer(rospy.Duration(0.1) , self.iterate)
    
    def distance_to_goal(self):
        return sqrt((self.target_x-self.pose.x)**2 +(self.target_y-self.pose.y)**2)
    

    def iterate(self,event):
        if self.target_x is not None and self.target_y is not None:
            # pass
            
            if (self.distance_to_goal() < self.tolorance):
                print(self.tolorance)
                self.target_x = None
                self.target_y = None
            else: 
                v_d , w_d  = self.move_to_pose()
                
                self.vel_msg.linear.x = v_d
                self.vel_msg.angular.z = w_d
                self.vel_pub.publish(self.vel_msg)


    def move_to_pose(self):
        d = self.distance_to_goal()
        psi_d = atan2(self.target_y - self.pose.y, self.target_x - self.pose.x)

        w_d = self.Kh*wrap_angle(psi_d-self.pose.theta)

        v_d = self.Kv*d
        return v_d, w_d
    

    def move_to_goal(self ,target_x , target_y ):
        
        self.target_x = target_x
        self.target_y = target_y
    def stop_turtlbot(self):
        self.vel_msg.linear.x = 0
        self.vel_msg.angular.z = 0
        self.vel_pub.publish(self.vel_msg)

if __name__ == '__main__':
    
    try:
       
       target_x = 1
       target_y = 1
       if(len(sys.argv) > 1):
            target_x = float(sys.argv[1])
            target_y = float(sys.argv[2])
       elif rospy.has_param("target_x") and rospy.has_param("target_y"):
           target_x = rospy.get_param("target_x") 
           target_y = rospy.get_param("target_y") 

       print(target_x, target_y)
       
       move = Move()
       
       move.move_to_goal(target_x , target_y)
       rospy.spin()
       
    except rospy.ROSInterruptException: pass
   
