#!/usr/bin/env python

import rospy, math
from geometry_msgs.msg import Twist
from ackermann_msgs.msg import AckermannDriveStamped

def convert_trans_rot_vel_to_steering_angle(v, omega, wheelbase):
  if omega == 0 or v == 0:
    return 0

  radius = v / omega
  return math.atan(wheelbase / radius)


def cmd_callback(data):
  global wheelbase
  global ackermann_cmd_topic
  global frame_id
  global pub
  
  v = data.linear.x*3
  steering = convert_trans_rot_vel_to_steering_angle(v, data.angular.z*2, wheelbase)
  
  msg = AckermannDriveStamped()
  msg.header.stamp = rospy.Time.now()
  msg.header.frame_id = frame_id
  msg.drive.steering_angle = steering
  msg.drive.speed = v
  
  pub.publish(msg)
  

if __name__ == '__main__': 
  try:
    
    rospy.init_node('cmd_vel_to_ackermann_drive')
        
    twist_cmd_topic = rospy.get_param('~twist_cmd_topic', '/cmd_vel') 
    # ackermann_cmd_topic = rospy.get_param('~ackermann_cmd_topic', '/ackermann_cmd')
    wheelbase = rospy.get_param('~wheelbase', 0.4)
    frame_id = rospy.get_param('~frame_id', 'odom')
    
    rospy.Subscriber(twist_cmd_topic, Twist, cmd_callback, queue_size=20)
    pub = rospy.Publisher( '/vesc/high_level/ackermann_cmd_mux/input/nav_0', AckermannDriveStamped, queue_size=20)
    
    rospy.loginfo("Node 'cmd_vel_to_ackermann_drive' started.\nListening to %s, publishing to %s. Frame id: %s, wheelbase: %f", "/cmd_vel", '/vesc/high_level/ackermann_cmd_mux/input/nav_0', frame_id, wheelbase)
    
    rospy.spin()
    
  except rospy.ROSInterruptException:
    pass