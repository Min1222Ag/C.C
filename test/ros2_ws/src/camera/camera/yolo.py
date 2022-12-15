#!/usr/bin/env python
# coding:utf-8
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
#from rclpy.qos import qos_profile_sensor_data
from std_msgs.msg import ByteMultiArray as yolo_arr

import torch
import os
#from models.experimental import attempt_load
#from edgetpu.detection.engine import DetectionEngine


#from PIL import Image
from PIL import Image as Img
from PIL import ImageTk
import time

import cv2
from cv_bridge import CvBridge

import imutils

model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
#model = torch.hub.load('WongKinYiu/yolov7', 'yolov7', pretrained=True)
#yolov7, yolov7x, yolov7-w6, yolov7-e6, yolov7-d6, yolov7-e6e

class Yolov7(Node):
  """
  Create an Yolov7 class, which is a subclass of the Node class.
  """
  def __init__(self):
    """
    Class constructor to set up the node
    """
    # Initiate the Node class's constructor and give it a name
    super().__init__('camera_node')
     
    # Create the subscriber for image. This subscriber will receive an Image
    # from the video_frames topic. The queue size is 100 messages.
    self.image_subscription = self.create_subscription(
            Image,
            '/image_raw',
            self.listener_callback, 
            1000)
    self.image_subscription # prevent unused variable warning
     
    # Used to convert between ROS and OpenCV images
    self.br = CvBridge()
   
    # Create the publisher about image messages . This publisher will pusblish an list
    # from CV_YOLO topic. The queue size is 100 messages.
    self.imgmsg_publisher = self.create_publisher(yolo_arr,'CV_YOLO',100)
    timer_period = 0.01  # seconds
    self.timer = self.create_timer(timer_period, self.yolo_publish) # call self.motor_publish()

  def yolo_publish(self):
    msg = yolo_arr()
    self.imgmsg_publisher.publish(msg)
    #self.get_logger().info('Publishing video through YOLO')
 
  def listener_callback(self, data):
    """
    Callback function.
    """
    # Display the message on the console
    self.get_logger().info('Receiving video frame')
    
    # Convert ROS Image message to OpenCV image
    current_frame = self.br.imgmsg_to_cv2(data)
    
    frame = current_frame #cv2.read()
    frame = imutils.resize(current_frame, width=600)
    ori = frame.copy()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = Img.fromarray(frame)
   
    start = time.time()
    results = model(frame)
    end = time.time()
    
    results.print()
    print(results.pandas().xyxy[0])
    r_img = results.render()
    img_with_boxes = r_img[0]
    cv2.imshow("Frem", img_with_boxes)

    #key = cv2.waitKey(1) & 0xFF
    #if key == ord("q"):
    #    break

    cv2.waitKey(1)
    print("=========================================================")
      
def main(args=None):
 
  # Initialize the rclpy library
  rclpy.init(args=args)
 
  # Create the node
  yolov7 = Yolov7()
  # Spin the node so the callback function is called.
  rclpy.spin(yolov7)
  
  # Destroy the node explicitly
  # (optional - otherwise it will be done automatically
  # when the garbage collector destroys the node object)
  yolov7.destroy_node()
 
  # Shutdown the ROS client library for Python
  rclpy.shutdown()
 
if __name__ == '__main__':
  main()
