#!/usr/bin/env python
# coding:utf-8
import sys

sys.path.append({})

import numpy as np
import rclpy
from rclpy.node import Node

from time import sleep
from sensor_msgs.msg import LaserScan
from interfaces import msg as interfaces_msg

#from sensor_msgs.msg import Image
#from bboxes_ex_msgs.msg import BoundingBoxes, BoundingBox
#from cv_bridge import CvBridge

import RPi.GPIO as GPIO
import time

from sensor_msgs.msg import Image #
import cv2 #
from cv_bridge import CvBridge #


#SPIN_QUEUE = [image_subscriber, stop_publisher]
#PERIOD = 0.01

class lidarDetect(Node):
	def __init__(self):
		super().__init__('obstacles_detect_node')
		
		# Subscription info
		self.subscription = self.create_subscription(
			LaserScan,
			'/scan',
			self.lidarScan,
			100),
		self.subscription
		
		# Publisher info
		self.publisher_stop = self.create_publisher(interfaces_msg.Stop, 'Stop', 100)
		timer_period = 0.05  # seconds
		self.timer = self.create_timer(timer_period, self.decision_callback)
		
		# Lidar data
		self.Lidar_Angle = 60
		self.Limit_Distance = 1
		
		# Proximity Sensor info
		self.distance = 0
		
		# Motor control
		self.Stop = False
		self.Left_Forward = True
		self.Left_Speed = 0.5
		self.Right_Forward = True
		self.Right_Speed = 0.5
		
		# Sum of obstacles per point
		self.Avoid_Left = 0
		self.Avoid_Front = 0
		self.Avoid_Right = 0
	
		
	# /scan subscribe to detect 	
	def lidarScan(self, msg):
		ranges = np.array(msg.ranges)
		self.Avoid_Left = 0
		self.Avoid_Front = 0
		self.Avoid_Right = 0
		
		# Divide three part of the front
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
		sleep(0.1)
		
	# publish Stop, Left_Speed, Right_Speed		
	def decision_callback(self):
		msg = interfaces_msg.Stop()
		msg.stop = self.Stop
		msg.lspeed = self.Left_Speed
		msg.rspeed = self.Right_Speed
		self.publisher_stop.publish(msg)
		
		
		if self.Avoid_Left > 10 and self.Avoid_Front > 10 and self.Avoid_Right > 10:
			self.proximity_sensor()
			if self.distance < 100:
				self.Stop = True
				self.Left_Speed = 0.0
				self.Right_Speed = 0.0
				msg.stop = self.Stop
				msg.lspeed = self.Left_Speed
				msg.rspeed = self.Right_Speed
				self.publisher_stop.publish(msg)
				sleep(0.3)
			else:
				self.Stop = False
				self.Left_Speed = 0.1
				self.Right_Speed = 0.1
				msg.lspeed = self.Left_Speed
				msg.rspeed = self.Right_Speed
				self.publisher_stop.publish(msg)
				sleep(0.3)
		elif self.Avoid_Left <= 10 and self.Avoid_Front > 10 and self.Avoid_Right > 10:
			self.proximity_sensor()
			self.Left_Speed = 0.1
			self.Right_Speed = 0.6
			msg.lspeed = self.Left_Speed
			msg.rspeed = self.Right_Speed
			self.publisher_stop.publish(msg)
			sleep(0.5)
		elif self.Avoid_Left > 10 and self.Avoid_Front > 10 and self.Avoid_Right <= 10:
			self.Left_Speed = 0.6
			self.Right_Speed = 0.1
			msg.lspeed = self.Left_Speed
			msg.rspeed = self.Right_Speed
			self.publisher_stop.publish(msg)
			sleep(0.5)
		elif self.Avoid_Left > 10 and self.Avoid_Front <= 10 and self.Avoid_Right > 10:
			self.Left_Speed = 0.1
			self.Right_Speed = 0.1
			msg.lspeed = self.Left_Speed
			msg.rspeed = self.Right_Speed
			self.publisher_stop.publish(msg)
			sleep(0.5)
			
		elif self.Avoid_Left > 10 and self.Avoid_Front <= 10 and self.Avoid_Right <= 10:
			self.Left_Speed = 0.4
			self.Right_Speed = 0.1
			msg.lspeed = self.Left_Speed
			msg.rspeed = self.Right_Speed
			self.publisher_stop.publish(msg)
			sleep(0.5)
		elif self.Avoid_Left <= 10 and self.Avoid_Front <= 10 and self.Avoid_Right > 10:
			self.Left_Speed = 0.1
			self.Right_Speed = 0.4
			msg.lspeed = self.Left_Speed
			msg.rspeed = self.Right_Speed
			self.publisher_stop.publish(msg)
			sleep(0.5)
		elif self.Avoid_Left <= 10 and self.Avoid_Front > 10 and self.Avoid_Right <= 10:
			self.Left_Speed = 0.1
			self.Right_Speed = 0.4
			msg.lspeed = self.Left_Speed
			msg.rspeed = self.Right_Speed
			self.publisher_stop.publish(msg)
			sleep(0.5)
		else:
			self.Stop = False
			self.Left_Speed = 0.5
			self.Right_Speed = 0.5
			msg.stop = self.Stop
			msg.lspeed = self.Left_Speed
			msg.rspeed = self.Right_Speed
			self.publisher_stop.publish(msg)
			sleep(0.5)
		print(msg)
	# set up the proximity sensor
	def proximity_sensor(self):
		try:
			GPIO.setmode(GPIO.BCM)
			
			PIN_TRIGGER = 23
			PIN_ECHO = 24
			
			GPIO.setup(PIN_TRIGGER, GPIO.OUT)
			GPIO.setup(PIN_ECHO, GPIO.IN)
			
			GPIO.output(PIN_TRIGGER, GPIO.LOW)
			time.sleep(0.01)
			GPIO.output(PIN_TRIGGER, GPIO.HIGH)
	
			time.sleep(0.0001)
			
			GPIO.output(PIN_TRIGGER, GPIO.LOW)
			
			pulse_start_time = time.time()
			pulse_end_time = time.time()
			
			while GPIO.input(PIN_ECHO) == 0:
				pulse_start_time = time.time()
			while GPIO.input(PIN_ECHO) == 1:
				pulse_end_time = time.time()
				
			pulse_duration = pulse_end_time - pulse_start_time
			self.distance = round(pulse_duration * 17150, 2)
			print("Distance:", self.distance, "cm")
		finally:
			GPIO.cleanup()		

class ImageSubscriber(Node):
  """
  Create an ImageSubscriber class, which is a subclass of the Node class.
  """
  def __init__(self):
    """
    Class constructor to set up the node
    """
    # Initiate the Node class's constructor and give it a name
    super().__init__('image_subscriber')
      
    # Create the subscriber. This subscriber will receive an Image
    # from the video_frames topic. The queue size is 10 messages.
    self.subscription = self.create_subscription(
      Image, 
      '/image_raw', 
      self.listener_callback, 
      10)
    self.subscription # prevent unused variable warning
      
    # Used to convert between ROS and OpenCV images
    self.br = CvBridge()
   
  def listener_callback(self, data):
    """
    Callback function.
    """
    # Display the message on the console
    self.get_logger().info('Receiving video frame')
 
    # Convert ROS Image message to OpenCV image
    current_frame = self.br.imgmsg_to_cv2(data)
    
    # Display image
    cv2.imshow("camera", current_frame)
    
    cv2.waitKey(1)

def main(args=None):
	rclpy.init(args=args)
	
	image_subscriber = ImageSubscriber()	# Create the node


	"""
	SPIN_QUEUE.append(Node()) 
	SPIN_QUEUE.append(Node()) 

	while rclpy.ok(): 
		try:
			for node in SPIN_QUEUE:
				rclpy.spin_once(node, timeout_sec=(PERIOD / len(spin_queue)))
		except Exception as e:
			print(f"something went wrong in the ROS Loop: {e}")
	"""

	obstacles_detect_node = lidarDetect()
	rclpy.spin(obstacles_detect_node)
	obstacles_detect_node.destroy_node()
	
	stop_publisher = StopPublisher()
	rclpy.spin(stop_publisher)
	stop_publisher.destroy_node()

	rclpy.spin(image_subscriber)
	image_subscriber.destroy_node()
	
	
	rclpy.shutdown()
    

if __name__ == '__main__':
	main()
