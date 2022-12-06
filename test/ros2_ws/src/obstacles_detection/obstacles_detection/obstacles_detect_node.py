#!/usr/bin/env python
# coding:utf-8
import numpy as np
import rclpy
from rclpy.node import Node
from time import sleep

# interfaces for publisher and subscription
from sensor_msgs.msg import LaserScan
from interfaces.msg import Stop
from std_msgs.msg import ByteMultiArray as yolo_arr  # for YOLO subscription message type

import RPi.GPIO as GPIO
import time

class lidarDetect(Node):
    def __init__(self):
        super().__init__('obstacles_detect_node'). # node name : obstacles_detect_node
        
        # Subscription info for LiDAR
        self.lidar_subscription = self.create_subscription(
            LaserScan,    # topic type
            '/scan',       # topic name : /scan
            self.lidarScan,  # callback function
            100),           # queue size
        self.lidar_subscription
       
        # Subscription info for YOLO  
        self.yolo_subscription = self.create_subscription(
            yolo_arr,    # topic type
            'CV_YOLO',    # topic name : CV_YOLO
            self.get_imgmsg,    #callback function
            100)            #queue size
        self.yolo_subscription
      
        
        # Publisher info
        self.publisher_stop = self.create_publisher(
            Stop,      # topic 
            'Stop',    #topic name : Stop
            10)        # queue size
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
        
        
        # Subscription callback function
    def get_imgmsg(self,msg):
        print("get_imgmsg opertated")
        print(msg)
        ### 
        # self.get_logger().info('I heard: "%d"' % msg.data)
        
        
        
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
            #print(self.Avoid_Left,self.Avoid_Front,self.Avoid_Right)
        sleep(0.1)
     
    # pulisher(timer) callback function
    # publish Stop, Left_Speed, Right_Speed 
    def decision_callback(self):
        msg = Stop()
        msg.stop = self.Stop
        msg.lspeed = self.Left_Forward #self.Left_Speed
        msg.rspeed = self.Right_Forward #self.Right_Speed
        
        
        if self.Avoid_Left > 10 and self.Avoid_Front > 10 and self.Avoid_Right > 10:
            self.proximity_sensor()
            if self.distance < 100: 
                #self.Left_Speed = 0.0
                #self.Right_Speed = 0.0
                self.Stop = True
                self.Left_Forward = False
                self.Right_Forward = False
                self.Avoid_Front += 10
                msg.stop = self.Stop
                msg.lspeed = self.Left_Forward
                msg.rspeed = self.Right_Forward
                #msg.lspeed = self.Left_Speed
                #msg.rspeed = self.Right_Speed
                self.publisher_stop.publish(msg)
                sleep(1)
            else:
                self.Stop = False
                self.Left_Forward = False
                self.Right_Forward = False
                #self.Left_Speed = 0.1
                #self.Right_Speed = 0.1
                msg.lspeed = self.Left_Forward
                msg.rspeed = self.Right_Forward
                self.publisher_stop.publish(msg)
                sleep(1)
        elif self.Avoid_Left <= 10 and self.Avoid_Front > 10 and self.Avoid_Right > 10:
            self.proximity_sensor()
            if self.distance < 100: 
                #self.Left_Speed = 0.0
                #self.Right_Speed = 0.0
                self.Stop = True
                self.Left_Forward = True 
                self.Right_Forward = False
                self.Avoid_Front += 10
                msg.stop = self.Stop
                msg.lspeed = self.Left_Forward
                msg.rspeed = self.Right_Forward
                #msg.lspeed = self.Left_Speed
                #msg.rspeed = self.Right_Speed
                self.publisher_stop.publish(msg)
                sleep(1)
            else:
                self.Stop = False
                self.Left_Forward = False
                self.Right_Forward = False
                #self.Left_Speed = 0.1
                #self.Right_Speed = 0.1
                msg.lspeed = self.Left_Forward
                msg.rspeed = self.Right_Forward
                self.publisher_stop.publish(msg)
                sleep(1)
            #self.Left_Speed = 0.1
            #self.Right_Speed = 0.6
            #msg.lspeed = self.Left_Speed
            #msg.rspeed = self.Right_Speed
            #self.publisher_stop.publish(msg)
            #sleep(0.5)
        elif self.Avoid_Left > 10 and self.Avoid_Front > 10 and self.Avoid_Right <= 10:
            self.proximity_sensor()
            if self.distance < 100:
                self.Stop = True
                self.Left_Forward = False
                self.Right_Forward = True
                self.Avoid_Front += 10
                msg.stop = self.Stop
                msg.lspeed = self.Left_Forward
                msg.rspeed = self.Right_Forward
                self.publisher_stop.publish(msg)
                sleep(1)
            else:
                self.Stop = False
                self.Left_Forward = False
                self.Right_Forward = True
                msg.lspeed = self.Left_Forward
                msg.rspeed = self.Right_Forward
                self.publisher_stop.publish(msg)
                sleep(1)
            #self.Left_Speed = 0.6
            #self.Right_Speed = 0.1
            #msg.lspeed = self.Left_Speed
            #msg.rspeed = self.Right_Speed
            #self.publisher_stop.publish(msg)
            #sleep(0.5)
        elif self.Avoid_Left > 10 and self.Avoid_Front <= 10 and self.Avoid_Right > 10:
            self.proximity_sensor()
            if self.distance < 100:
                self.Stop = True
                self.Left_Forward = False
                self.Right_Forward = False
                self.Avoid_Front += 10
                msg.stop = self.Stop
                msg.lspeed = self.Left_Forward
                msg.rspeed = self.Right_Forward
                self.publisher_stop.publish(msg)
                sleep(1)
            else:
                self.Stop = False
                self.Left_Forward = False
                self.Right_Forward = False
                msg.lspeed = self.Left_Forward
                msg.rspeed = self.Right_Forward
                self.publisher_stop.publish(msg)
                sleep(1)
            #self.Left_Speed = 0.1
            #self.Right_Speed = 0.1
            #msg.lspeed = self.Left_Speed
            #msg.rspeed = self.Right_Speed
            #self.publisher_stop.publish(msg)
            #sleep(1)
            
        elif self.Avoid_Left > 10 and self.Avoid_Front <= 10 and self.Avoid_Right <= 10:
            self.proximity_sensor()
            if self.distance < 100:
                self.Stop = True
                self.Left_Forward = False
                self.Right_Forward = True
                self.Avoid_Front += 10
                msg.stop = self.Stop
                msg.lspeed = self.Left_Forward
                msg.rspeed = self.Right_Forward
                self.publisher_stop.publish(msg)
                sleep(1)
            else:
                self.Stop = False
                self.Left_Forward = False
                self.Right_Forward = True
                msg.lspeed = self.Left_Forward
                msg.rspeed = self.Right_Forward
                self.publisher_stop.publish(msg)
                sleep(1)
            #self.Left_Speed = 0.4
            #self.Right_Speed = 0.1
            #msg.lspeed = self.Left_Speed
            #msg.rspeed = self.Right_Speed
            #self.publisher_stop.publish(msg)
            #sleep(0.5)
            
        elif self.Avoid_Left <= 10 and self.Avoid_Front <= 10 and self.Avoid_Right > 10:
            self.proximity_sensor()
            if self.distance < 100:
                self.Stop = True
                self.Left_Forward = True
                self.Right_Forward = False
                self.Avoid_Front += 10
                msg.stop = self.Stop
                msg.lspeed = self.Left_Forward
                msg.rspeed = self.Right_Forward
                self.publisher_stop.publish(msg)
                sleep(1)
            else:
                self.Stop = False
                self.Left_Forward = True
                self.Right_Forward = False
                msg.lspeed = self.Left_Forward
                msg.rspeed = self.Right_Forward
                self.publisher_stop.publish(msg)
                sleep(1)
            #self.Left_Speed = 0.1
            #self.Right_Speed = 0.4
            #msg.lspeed = self.Left_Speed
            #msg.rspeed = self.Right_Speed
            #self.publisher_stop.publish(msg)
            #sleep(0.5)
            
        elif self.Avoid_Left <= 10 and self.Avoid_Front > 10 and self.Avoid_Right <= 10:
            self.proximity_sensor()
            if self.distance < 100:
                self.Stop = True
                self.Left_Forward = True
                self.Right_Forward = True
                self.Avoid_Front += 10
                msg.stop = self.Stop
                msg.lspeed = self.Left_Forward
                msg.rspeed = self.Right_Forward
                self.publisher_stop.publish(msg)
                sleep(1)
            else:
                self.Stop = False
                self.Left_Forward = True
                self.Right_Forward = True
                msg.lspeed = self.Left_Forward
                msg.rspeed = self.Right_Forward
                self.publisher_stop.publish(msg)
                sleep(1)
            #self.Left_Speed = 0.1
            #self.Right_Speed = 0.4
            #msg.lspeed = self.Left_Speed
            #msg.rspeed = self.Right_Speed
            #self.publisher_stop.publish(msg)
            #sleep(0.5)
            
        else:
            self.Stop = False
            self.Left_Forward = True
            self.Right_Forward = True
            msg.lspeed = self.Left_Forward
            msg.rspeed = self.Right_Forward
            self.publisher_stop.publish(msg)
            
            #self.Left_Speed = 0.5
            #self.Right_Speed = 0.5
            #msg.lspeed = self.Left_Speed
            #msg.rspeed = self.Right_Speed
            #self.publisher_stop.publish(msg)
            sleep(1)
            
        print(msg)
        #self.Stop = False
        #self.publisher_stop.publish(msg)
        #print(msg)
        
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
           
def main(args=None):
    rclpy.init(args=args)
    
    # for the LiDAR detection
    obstacles_detect_node = lidarDetect()
    rclpy.spin(obstacles_detect_node)
    obstacles_detect_node.destroy_node()
    
    # for publisher node
    stop_publisher = StopPublisher()
    rclpy.spin(stop_publisher)
    stop_publisher.destroy_node()
    
    
    rclpy.shutdown()
    
if __name__ == '__main__': 
    main()
  
