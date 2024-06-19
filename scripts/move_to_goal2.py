
#!/usr/bin/env python3


# to reach a point the robot rotates firsst then moves to 
# the desired point straight line 

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
        self.Kw=  1  # Angular Velocity Constant
        self.Kv = 1 # Linear Velocity Constant
        self.target_x = target_x 
        self.target_y = target_y

        rospy.init_node('move_to_pose', anonymous=True)
        self.Rate = rospy.Rate(10)

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
    
    # set a new goal
    def set_goal(self ,target_x , target_y ):
       
        self.target_x = target_x
        self.target_y = target_y
    def move_to_goal(self):
        time.sleep(0.7)
        
        delta_x =  round(self.target_x - self.pose.x ,4)
        delta_y =  round(self.target_y - self.pose.y ,4)

        print( self.pose.x , self.pose.y , self.target_x ,self.target_y , delta_x,delta_y)
        angle = atan2(delta_y,delta_x)
        relative_angle_degree = degrees(angle)
        print(relative_angle_degree , angle )
        angle =  wrap_angle(angle - self.pose.theta)
        print( self.pose.theta ,degrees(self.pose.theta), angle , degrees(angle) )
        current_angle = 0
        t0 = rospy.Time.now().to_sec()

        # Rotate the turtle to the desired angle
        while  current_angle < abs(angle):

            angular_vel = self.Kw
            t1 = rospy.Time.now().to_sec()
            if(angle < 0 ):
                angular_vel = -angular_vel
            current_angle = (t1-t0)*abs(angular_vel)
            self.vel_msg.linear.x = 0
            self.vel_msg.linear.y = 0
            self.vel_msg.linear.z = 0

            self.vel_msg.angular.x = 0
            self.vel_msg.angular.y = 0
            self.vel_msg.angular.z = angular_vel
        
            self.vel_pub.publish(self.vel_msg)
        

        # Move the turtle to the desired position
        t0 = rospy.Time.now().to_sec()
        total_distance = 0 
        distance = self.distance_to_goal()
        while  total_distance < distance:

            linear_speed = 1
            t1 = rospy.Time.now().to_sec()
            if(angle < 0 ):
                linear_speed = 1
            total_distance = (t1-t0)*abs(linear_speed)
            self.vel_msg.linear.x = linear_speed
            self.vel_msg.linear.y = 0
            self.vel_msg.linear.z = 0

            self.vel_msg.angular.x = 0
            self.vel_msg.angular.y = 0
            self.vel_msg.angular.z = 0
            self.vel_pub.publish(self.vel_msg)

        self.vel_msg.linear.x = 0
        self.vel_msg.angular.z = 0
        self.vel_pub.publish(self.vel_msg)


if __name__ == '__main__':
    
    target_x = 1
    target_y = 1
    try:
       if(len(sys.argv) > 1):
            target_x = float(sys.argv[1])
            target_y = float(sys.argv[2])
       elif rospy.has_param("target_x") and rospy.has_param("target_y"):
           target_x = rospy.get_param("target_x") 
           target_y = rospy.get_param("target_y") 
  
       move = Move(target_x , target_y)
       move.move_to_goal()
    
       rospy.spin()
       
    except rospy.ROSInterruptException: pass
   
