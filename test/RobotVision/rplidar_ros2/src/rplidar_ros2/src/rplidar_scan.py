#!/usr/bin/env python
# coding:utf-8
import numpy as np
import rclpy
from rclpy.node import Node

from time import sleep
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan, String

class lidarDetect(Node):
	def __init__(self):
		super().__init__('rplidar_detector_node')
		self.subscription = self.create_subscription(
			LaserScan,
			'/scan',
			self.lidarScan,
			100)
		self.subscription
		
		self.publisher_stop = self.create_publisher(String, 'Stop', 10)
		
		self.Lidar_Angle = 60
		self.Limit_Distance = 1
		
		self.Stop = False
		self.Left_Forward = True
		self.Left_Speed = 0.1
		self.Right_Forward = True
		self.Right_Speed = 0.1
		
		self.Avoid_Left = 0
		self.Avoid_Front = 0
		self.Avoid_Right = 0
		
		
	def lidarScan(self, msg):
		ranges = np.array(msg.ranges)
		self.Avoid_Left = 0
		self.Avoid_Front = 0
		self.Avoid_Right = 0
		
		for i in range(len(ranges)):
			if 10 < i < self.Lidar_Angle:
				if ranges[i] < self.Limit_Distance: 
					self.Avoid_Left += 1
			elif (340 - self.Lidar_Angle) < i < 350:
				if ranges[i] < self.Limit_Distance: 
					self.Avoid_Right += 1
			elif (340 <= i <= 360) or (0<= i <=20):
				if ranges[i] < self.Limit_Distance: 
					self.Avoid_Front += 1
			print(self.Avoid_Left,self.Avoid_Front,self.Avoid_Right)
			
	def decision_driving(self):
		msg = String()
		msg.data = '%s' % self.Stop
		while not rclpy.shutdown():
			if self.Avoid_Left > 10 and self.Avoid_Front > 10 and self.Avoid_Right > 10:
				self.Stop = True
				self.publisher_stop.publish(msg)
				


def main(args=None):
	rclpy.init(args=args)
	
	rplidar_detector_node = lidarDetect()
	rclpy.spin(rplidar_detector_node)
	rplidar_detector_node.destroy_node()
	
	stop_publisher = StopPublisher()
	rclpy.spin(stop_publisher)
	stop_publisher.destroy_node()
	
	
	rclpy.shutdown()
    

if __name__ == '__main__':
	main()
    
