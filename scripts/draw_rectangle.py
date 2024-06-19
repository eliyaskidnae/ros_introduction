#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
PI = 3.1415926535897
pose_x = 0
pose_y = 0
pose_theta = 0

def callback(req):
   global pose_x,pose_y,pose_theta
   pose_x = req.x
   pose_y = req.y
   pose_theta = req.theta

def draw_rec():
    global pose_x,pose_y,pose_theta
    #Starts a new node
    rospy.init_node('robot_cleaner', anonymous=True)

    # publisher
    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)

    #subscriber
    sub = rospy.Subscriber('/turtle1/pose',Pose,callback)
    vel_msg = Twist()

    # Receiveing the user's input
    rect_side = input("Input Rectangle Side ():")

    rect_side = float(rect_side)
    speed = 1
    #We wont use linear components
    vel_msg.linear.x=0
    vel_msg.linear.y=0
    vel_msg.linear.z=0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    current_dis = 0 
    relative_angle = 0
    # print(current_dis)3
    r = rospy.Rate(1000)
    while not rospy.is_shutdown():
        
        # Rotate Pi/2 b.ce recangle sides has Pi/2 gegrees
        t0 = rospy.Time.now().to_sec()
        while current_dis < rect_side:
            t1 = rospy.Time.now().to_sec()
            current_dis = (t1-t0)*speed
            
            vel_msg.linear.x = speed
            velocity_publisher.publish(vel_msg)
            r.sleep()


        # move the turtle to draw on side of the rectangle 
        t0 = rospy.Time.now().to_sec()
        while relative_angle < PI/2:
            t1 = rospy.Time.now().to_sec()
            relative_angle = (t1-t0)*0.5
            vel_msg.angular.z = 0.5
            vel_msg.linear.x = 0 
            velocity_publisher.publish(vel_msg)
            r.sleep() 
            

        vel_msg.linear.x = 0
        vel_msg.angular.z = 0
        current_dis = 0
        relative_angle = 0
        velocity_publisher.publish(vel_msg)
        

if __name__ == '__main__':
    try:
        # Testing our function
        draw_rec()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass