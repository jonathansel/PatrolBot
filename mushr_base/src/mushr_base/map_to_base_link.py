#!/usr/bin/env python
import rospy #ROS python functionality
import numpy as np
import tf
from tf.transformations import euler_from_quaternion, quaternion_from_euler
import tf2_ros #Transform listener
import math
import time
from std_msgs.msg import UInt16, Int32 #Init UInt16 and UInt32 msg type

robot_trans_x = 0
robot_trans_y = 0
robot_rot_w = 0
robot_rot_z = 0

#Init ROS node and tf2 listener
rospy.init_node("map_to_base_link")
tfBuffer = tf2_ros.Buffer()
listener = tf2_ros.TransformListener(tfBuffer)

r = rospy.Rate(4)

# While loop to transform robot base_footprint to map frame (tf2 listener)
while not rospy.is_shutdown():
    
    try:
        transformObject = tfBuffer.lookup_transform('map', 'base_link', rospy.Time())
        trans = transformObject.transform.translation
        rot = transformObject.transform.rotation
        
    except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
        r.sleep()
        continue    

    #Set global vars to found x,y position and quarternion rotation
    robot_trans_x = trans.x
    robot_trans_y = trans.y
    robot_rot_z = rot.z
    robot_rot_w = rot.w
    print(robot_trans_x)

    r.sleep()