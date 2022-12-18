#!/usr/bin/env python
# coding:utf-8

# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/usr/bin/env python
# coding:utf-8
import numpy as np
import rclpy
from rclpy.node import Node
from time import sleep

from sensor_msgs.msg import LaserScan
from interfaces.msg import Stop


from std_msgs.msg import ByteMultiArray as yolo_arr  # for YOLO subscription message type

import RPi.GPIO as GPIO
import time

# define lidarDetect node
class lidarDetect(Node):
    def __init__(self):
        super().__init__('obstacles_detect_node')
        
        # Subscription info for LiDAR
        self.lidar_subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.lidarScan,
            100),
        self.lidar_subscription
       
        # Subscription info for YOLO  
        self.yolo_subscription = self.create_subscription(yolo_arr, 'CV_YOLO', self.get_imgmsg, 100)
        self.yolo_subscription
      
        
        
        # Publisher info
        self.publisher_stop = self.create_publisher(Stop, 'Stop', 10)
        timer_period = 0.05  # seconds
        self.timer = self.create_timer(timer_period, self.decision_callback)
        
        # Lidar data
        self.Lidar_Angle = 60
        self.Limit_Distance = 23
        
        # Proximity Sensor distance info
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
        #print(msg)
        ### 
        # self.get_logger().info('I heard: "%d"' % msg.data)
        
        
        
    # /scan subscribe to detect 
    def lidarScan(self, msg):
        ranges = np.array(msg.ranges)
        self.Avoid_Left = 0
        self.Avoid_Front = 0
        self.Avoid_Right = 0

    # Divide into three front part of the robot and voting ranges 
        for i in range(len(ranges)):
            if 10 < i < self.Lidar_Angle:
                if ranges[i] < self.Limit_Distance: 
                    self.Avoid_Left += 1
            elif (340 - self.Lidar_Angle) < i < 350:
                if ranges[i] < self.Limit_Distance: 
                    self.Avoid_Right += 1
            elif (330 <= i <= 360) or (0<= i <=30):
                if ranges[i] < self.Limit_Distance: 
                    self.Avoid_Front += 1
            #print(self.Avoid_Left,self.Avoid_Front,self.Avoid_Right)
        sleep(0.1)
        
   
    # 1. Using Sum of obstacles per point
    # 2. Using proximity sensor
    # publish msg(Stop, Left_Speed, Right_Speed)
    def decision_callback(self):
        msg = Stop()
        msg.stop = self.Stop
        msg.lspeed = self.Left_Forward #self.Left_Speed
        msg.rspeed = self.Right_Forward #self.Right_Speed
        
        # All dangerous cases
        if self.Avoid_Left > 10 and self.Avoid_Front > 10 and self.Avoid_Right > 10:
            self.proximity_sensor()
            if self.distance < 200: 
                self.Stop = True
                self.Left_Forward = False
                self.Right_Forward = False
                self.Avoid_Front += 10
                msg.stop = self.Stop
                msg.lspeed = self.Left_Forward
                msg.rspeed = self.Right_Forward
                self.publisher_stop.publish(msg)
                sleep(1)
            # except, but warning sign    
            else:
                self.Stop = False
                self.Left_Forward = False
                self.Right_Forward = False
                msg.lspeed = self.Left_Forward
                msg.rspeed = self.Right_Forward
                self.publisher_stop.publish(msg)
                sleep(1)
        # Completely Avoid to the Left
        elif self.Avoid_Left <= 10 and self.Avoid_Front > 10 and self.Avoid_Right > 10:
            self.proximity_sensor()
            if self.distance < 200: 
                self.Stop = True
                self.Left_Forward = True 
                self.Right_Forward = False
                self.Avoid_Front += 10
                msg.stop = self.Stop
                msg.lspeed = self.Left_Forward
                msg.rspeed = self.Right_Forward
                self.publisher_stop.publish(msg)
                sleep(1)
            # except, but warning sign      
            else:
                self.Stop = False
                self.Left_Forward = False
                self.Right_Forward = False
                msg.lspeed = self.Left_Forward
                msg.rspeed = self.Right_Forward
                self.publisher_stop.publish(msg)
                sleep(1)
        # Completely Avoid to the Right    
        elif self.Avoid_Left > 10 and self.Avoid_Front > 10 and self.Avoid_Right <= 10:
            self.proximity_sensor()
            if self.distance < 200:
                self.Stop = True
                self.Left_Forward = False
                self.Right_Forward = True
                self.Avoid_Front += 10
                msg.stop = self.Stop
                msg.lspeed = self.Left_Forward
                msg.rspeed = self.Right_Forward
                self.publisher_stop.publish(msg)
                sleep(1)
            # except, but warning sign      
            else:
                self.Stop = False
                self.Left_Forward = False
                self.Right_Forward = True
                msg.lspeed = self.Left_Forward
                msg.rspeed = self.Right_Forward
                self.publisher_stop.publish(msg)
                sleep(1)
        # Stop    
        elif self.Avoid_Left > 10 and self.Avoid_Front <= 10 and self.Avoid_Right > 10:
            self.proximity_sensor()
            if self.distance < 200:
                self.Stop = True
                self.Left_Forward = False
                self.Right_Forward = False
                self.Avoid_Front += 10
                msg.stop = self.Stop
                msg.lspeed = self.Left_Forward
                msg.rspeed = self.Right_Forward
                self.publisher_stop.publish(msg)
                sleep(1)
            # except, but warning sign      
            else:
                self.Stop = False
                self.Left_Forward = False
                self.Right_Forward = False
                msg.lspeed = self.Left_Forward
                msg.rspeed = self.Right_Forward
                self.publisher_stop.publish(msg)
                sleep(1)
        # Avoid to the Right    
        elif self.Avoid_Left > 10 and self.Avoid_Front <= 10 and self.Avoid_Right <= 10:
            self.proximity_sensor()
            if self.distance < 200:
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
        # Avoid to the Left  
        elif self.Avoid_Left <= 10 and self.Avoid_Front <= 10 and self.Avoid_Right > 10:
            self.proximity_sensor()
            if self.distance < 200:
                self.Stop = True
                self.Left_Forward = True
                self.Right_Forward = False
                self.Avoid_Front += 10
                msg.stop = self.Stop
                msg.lspeed = self.Left_Forward
                msg.rspeed = self.Right_Forward
                self.publisher_stop.publish(msg)
                sleep(1)
            # except, but warning sign  
            else:
                self.Stop = False
                self.Left_Forward = True
                self.Right_Forward = False
                msg.lspeed = self.Left_Forward
                msg.rspeed = self.Right_Forward
                self.publisher_stop.publish(msg)
                sleep(1)
            
        # Slowly   
        elif self.Avoid_Left <= 10 and self.Avoid_Front > 10 and self.Avoid_Right <= 10:
            self.proximity_sensor()
            if self.distance < 200:
                self.Stop = True
                self.Left_Forward = True
                self.Right_Forward = True
                self.Avoid_Front += 10
                msg.stop = self.Stop
                msg.lspeed = self.Left_Forward
                msg.rspeed = self.Right_Forward
                self.publisher_stop.publish(msg)
                sleep(1)
            # except
            else:
                self.Stop = False
                self.Left_Forward = True
                self.Right_Forward = True
                msg.lspeed = self.Left_Forward
                msg.rspeed = self.Right_Forward
                self.publisher_stop.publish(msg)
                sleep(1)
        # Driving    
        else:
            self.Stop = False
            self.Left_Forward = True
            self.Right_Forward = True
            msg.lspeed = self.Left_Forward
            msg.rspeed = self.Right_Forward
            self.publisher_stop.publish(msg)
            
            sleep(1)
            
        print(msg)
        
    # set up the proximity sensor
    def proximity_sensor(self):
       try:
           # GPIO settings
           GPIO.setwarnings(False)
           GPIO.setmode(GPIO.BCM)
           PIN_TRIGGER = 17
           PIN_ECHO = 27
           
           GPIO.setup(PIN_TRIGGER, GPIO.OUT)
           GPIO.setup(PIN_ECHO, GPIO.IN)
           
           GPIO.output(PIN_TRIGGER, GPIO.LOW)
           time.sleep(2)
           GPIO.output(PIN_TRIGGER, GPIO.HIGH)
           time.sleep(0.0001)
         
           GPIO.output(PIN_TRIGGER, GPIO.LOW)
          
           pulse_start_time = time.time()
           pulse_end_time = time.time()
           
           # Calculated distance from Proximity sensor 
           while GPIO.input(PIN_ECHO) == 0:
                pulse_start_time = time.time()
           while GPIO.input(PIN_ECHO) == 1:
                pulse_end_time = time.time()
             
           pulse_duration = pulse_end_time - pulse_start_time
           self.distance = round(pulse_duration * 17150, 2)
           print("Distance:", self.distance)
       finally:
           GPIO.cleanup()
       time.sleep(1)
           
def main(args=None):
    rclpy.init(args=args)
    
    # execute node(subscribe and publish)
    obstacles_detect_node = lidarDetect()
    rclpy.spin(obstacles_detect_node)
    obstacles_detect_node.destroy_node()
    
    stop_publisher = StopPublisher()
    rclpy.spin(stop_publisher)
    stop_publisher.destroy_node()
   
    rclpy.shutdown()
    
if __name__ == '__main__': 
    main()
  
