#!/usr/bin/env python
# coding:utf-8
import numpy as np
from time import sleep
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class lidarDetect:
	def __init__(self):
			rospy.on_shutdown(self.cancel)
			self.Stop = False
			self.Left_Forward = True
			self.Left_Speed = 0.1
			self.Right_Forward = True
			self.Right_Speed = 0.1
			self.ros_ctrl = ROSCtrl()
			self.sub_laser = rospy.Subscriber('/scan', LaserScan, self.registerScan)
			#Server(laserAvoidPIDConfig, self.dynamic_reconfigure_callback)

	def cancel(self):
        self.ros_ctrl.cancel()
        self.sub_laser.unregister()
        rospy.loginfo("Shutting down this node.")
        
    

if __name__ == '__main__':
    rospy.init_node('lidar_obstacle_detection', anonymous=False)
    rplidar = lidarDetect()
    #rplidar.robot_move()
    rospy.spin()
    rplidar.cancel()
