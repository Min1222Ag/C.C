#!/usr/bin/env python
# coding:utf-8
import numpy as np
import rclpy
from rclpy.node import Node

from time import sleep
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class lidarDetect(Node):
	def __init__(self):
		super().__init__('rplidar_detector_node')
		self.subscription = self.create_subscription(
			LaserScan,
			'/scan',
			self.lidarScan,
			100)
		self.subscription
		self.Lidar_Angle = 10
		self.Limit_Distance = 0.5
		
		self.Stop = False
		self.Left_Forward = True
		self.Left_Speed = 0.1
		self.Right_Forward = True
		self.Right_Speed = 0.1
		
		self.Avoid_Left = 0
		self.Avoid_Front = 0
		self.Avoid_Right = 0
		
		#self.sub_laser = rclpy.Subscriber('/scan', LaserScan, self.registerScan)
		
	def listener_callback(self, msg):
		self.get_logger().info('I heard: "%s"' %msg.ranges)
		
	def lidarScan(self, msg):
		ranges = np.array(msg.ranges)
		#sortedIndices = np.argsort(ranges)
		self.Avoid_Left = 0
		self.Avoid_Front = 0
		self.Avoid_Right = 0
		
		for i in range(len(ranges)):
			#print("i: ", i, "dist: ", ranges[i])
			if 10 < i < self.Lidar_Angle:
				if ranges[i] < self.Limit_Distance: 
					self.Avoid_Left += 1
			elif (350 - self.Lidar_Angle) < i < 350:
				if ranges[i] < self.Limit_Distance: 
					self.Avoid_Right += 1
			elif (350 <= i <= 360) or (0<= i <=10):
				if ranges[i] < self.Limit_Distance: 
					self.Avoid_Front += 1
			print(self.Avoid_Left,self.Avoid_Front,self.Avoid_Right)


def main(args=None):
	rclpy.init(args=args)
	rplidar_detector_node = lidarDetect()
	
	rclpy.spin(rplidar_detector_node)
	rplidar_detector_node.destroy_node()
	rclpy.shutdown()
    

if __name__ == '__main__':
	main()
    
