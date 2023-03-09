#!/usr/bin/env python3

import rospy, math
from geometry_msgs.msg import Twist
from ackermann_msgs.msg import AckermannDriveStamped

def clip(value, lower, upper):
    return lower if value < lower else upper if value > upper else value

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
  
  v = data.linear.x
  steering = convert_trans_rot_vel_to_steering_angle(v, data.angular.z, wheelbase)
  steering_clipped = clip(steering, -0.55, 0.55) # True min max is 0.61
  print(steering_clipped) 
  msg = AckermannDriveStamped()
  msg.header.stamp = rospy.Time.now()
  msg.header.frame_id = frame_id
  msg.drive.steering_angle = steering_clipped
  msg.drive.speed = v
  pub_ego.publish(msg)
  

if __name__ == '__main__': 
  try:
    
    rospy.init_node('cmd_vel_to_ackermann_drive')
    wheelbase = rospy.get_param('~wheelbase', 0.85)
    frame_id = rospy.get_param('~frame_id', 'odom') 
    
    rospy.Subscriber('/cmd_vel', Twist, cmd_callback, queue_size=1)
    pub_ego = rospy.Publisher('/car/mux/ackermann_cmd_mux/input/navigation', AckermannDriveStamped, queue_size=1)
    rospy.spin()
    
  except rospy.ROSInterruptException:
    pass