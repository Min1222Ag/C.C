#!/usr/bin/env python
# coding:utf-8
import numpy as np
import rclpy
from rclpy.node import Node

from time import sleep
from sensor_msgs.msg import LaserScan
from interfaces.msg import Stop

class lidarDetect(Node):
	def __init__(self):
		super().__init__('rplidar_detector_node')
		self.subscription = self.create_subscription(
			LaserScan,
			'/scan',
			self.lidarScan,
			100)
		self.subscription
		
		self.publisher_stop = self.create_publisher(Stop, 'Stop', 10)
		timer_period = 0.1  # seconds
		self.timer = self.create_timer(timer_period, self.decision_driving)
		
		self.Lidar_Angle = 60
		self.Limit_Distance = 1
		
		self.Stop = False
		self.Left_Forward = True
		self.Left_Speed = 0.5
		self.Right_Forward = True
		self.Right_Speed = 0.5
		
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
		msg = Stop()
		msg.stop = self.Stop
		
		lspeed_msg = LSpeed()
		lspeed_msg.lspeed = self.Left_Speed
		
		rspeed_msg = RSpeed()
		rspeed_msg.rspeed = self.Right_Speed
		
		while not rclpy.shutdown():
			if self.Avoid_Left > 10 and self.Avoid_Front > 10 and self.Avoid_Right > 10:
				self.Stop = True
				self.publisher_stop.publish(msg)
				sleep(0.3)
			elif self.Avoid_Left <= 10 and self.Avoid_Front > 10 and self.Avoid_Right > 10:
				self.Left_Speed = 0.1
				self.Right_Speed = 0.6
				#self.publisher_lspeed.publish(lspeed_msg)
				#self.publisher rspeed.pubish(rspeed_msg)
				sleep(0.5)
			elif self.Avoid_Left > 10 and self.Avoid_Front > 10 and self.Avoid_Right <= 10:
				self.Left_Speed = 0.6
				Self.Right_Speed = 0.1
				#self.publisher_lspeed.publish(lspeed_msg)
				#self.publisher rspeed.pubish(rspeed_msg)
				sleep(0.5)
			elif self.Avoid_Left > 10 and self.Avoid_Front <= 10 and self.Avoid_Right > 10:
				self.Left_Speed = 0.1
				Self.Right_Speed = 0.1
				#self.publisher_lspeed.publish(lspeed_msg)
				#self.publisher rspeed.pubish(rspeed_msg)
				sleep(0.5)
				
			elif self.Avoid_Left > 10 and self.Avoid_Front <= 10 and self.Avoid_Right <= 10:
				self.Left_Speed = 0.4
				Self.Right_Speed = 0.1
				#self.publisher_lspeed.publish(lspeed_msg)
				#self.publisher rspeed.pubish(rspeed_msg)
				sleep(0.5)
			elif self.Avoid_Left <= 10 and self.Avoid_Front <= 10 and self.Avoid_Right > 10:
				self.Left_Speed = 0.4
				Self.Right_Speed = 0.1
				#self.publisher_lspeed.publish(lspeed_msg)
				#self.publisher rspeed.pubish(rspeed_msg)
				sleep(0.5)
			elif self.Avoid_Left <= 10 and self.Avoid_Front > 10 and self.Avoid_Right <= 10:
				self.Left_Speed = 0.1
				Self.Right_Speed = 0.4
				#self.publisher_lspeed.publish(lspeed_msg)
				#self.publisher rspeed.pubish(rspeed_msg)
				sleep(0.5)	
				


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
    
