#!/usr/bin/env python3

import rospy
import math
from ackermann_msgs.msg import AckermannDriveStamped
from std_msgs.msg import Float64

def clip(value, lower, upper):
    return lower if value < lower else upper if value > upper else value

def convert_trans_rot_vel_to_steering_angle(v, omega, wheelbase):
    if omega == 0 or v == 0:
        return 0

    radius = v / omega
    return math.atan(wheelbase / radius)

"""
cmd_callback: To direct joystick command of type 
    AckermannDriveStamped to respective joint commands 
    of Gazebo model
"""
def cmd_callback(data):
    steering = data.drive.steering_angle
    pub_ls.publish(steering)
    pub_rs.publish(steering)

    # Currently output of joystick velocity is 1.5m/s but too low for model. 
    v = data.drive.speed * 10
    # pub_fr_v.publish(v)
    # pub_fl_v.publish(v)
    pub_rr_v.publish(v)
    pub_rl_v.publish(v)

if __name__ == '__main__': 
  try:
    rospy.init_node('cmd_to_joint')
    print("Node for correlating joystick commands to gazebo model joint commands.\n")
    print("Use mushr_base/offline.launch with joystick connected to computer to use")
    rospy.Subscriber('/car/mux/ackermann_cmd_mux/output', AckermannDriveStamped, cmd_callback, queue_size=1)

    # publish to respective joint controllers - huge assumption: same velocity for all wheels and same steering angle for both left and right wheels
    pub_ls = rospy.Publisher('/patrol_robot/left_steer_position_controller/command', Float64, queue_size=1)
    pub_rs = rospy.Publisher('/patrol_robot/right_steer_position_controller/command', Float64, queue_size=1)

    # pub_fr_v = rospy.Publisher('/patrol_robot/front_right_velocity_controller/command', Float64, queue_size=1)
    # pub_fl_v = rospy.Publisher('/patrol_robot/front_left_velocity_controller/command', Float64, queue_size=1)
    pub_rr_v = rospy.Publisher('/patrol_robot/rear_right_velocity_controller/command', Float64, queue_size=1)
    pub_rl_v = rospy.Publisher('/patrol_robot/rear_left_velocity_controller/command', Float64, queue_size=1)

    rospy.spin()
    
  except rospy.ROSInterruptException:
    pass