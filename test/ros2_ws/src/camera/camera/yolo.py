#!/usr/bin/env python
# coding:utf-8
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from rclpy.qos import qos_profile_sensor_data   # for the proper queue size
from std_msgs.msg import ByteMultiArray as yolo_arr # topic type for yolo array

import torch

#import argparse

import time

import cv2
from cv_bridge import CvBridge 

class Yolov7(Node):
  """
  Create an Yolov7 class, which is a subclass of the Node class.
  """
  def __init__(self):
    """
    Class constructor to set up the node
    """
    # initiate the Node class's constructor
    super().__init__('camera_node'). # node name : camera_node
     
    
    # subscription for image
    self.image_subscription = self.create_subscription(
            Image,     # topic type : Image
            '/image_raw',     # topic name : /image_raw
            self.listener_callback,     # callback function
            qos_profile_sensor_data)    # queue size
    self.image_subscription # prevent unused variable warning
     
    # Used to convert between ROS and OpenCV images
    self.br = CvBridge()
   
    # Create the publisher about image messages as a list
    self.imgmsg_publisher = self.create_publisher(
      yolo_arr,      # topic type : yolo_arr
      'CV_YOLO',     # topic name : CV_YOLO
      100)          # queue size : 100
    timer_period = 0.01  # seconds
    self.timer = self.create_timer(timer_period, self.yolo_publish) # call self.motor_publish()

  def yolo_publish(self):
    msg = yolo_arr()
    self.imgmsg_publisher.publish(msg)
    self.get_logger().info('Publishing video through YOLO')
 
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
    
    
    labels = {}
   
    for row in open("/home/pi/C.C/test/ros2_ws/src/camera/camera/labels.txt"):
        (classID, label) = row.strip().split(maxsplit=1)
        labels[int(classID)] = label.strip()
    
    #model = torch.load('/home/pi/C.C/test/ros2_ws/src/camera/camera/best.pt')   
    #model = DetectionEngine("best.pt")
    #model = attempt_load('best.pt', map_location='cuda:0')
    #device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    #model = torch.load('ultralytics/yolov7', 'best.pt')
    
    #model = custom(path_or_model='best.pt')
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt', force_reload=True)
    #model = torch.hub.load(os.getcwd(), 'custom', path = 'best.pt',source='local')
    
    frame = current_frame #cv2.read()
    frame = imutils.resize(frame, width=600)
    ori = frame.copy()
   
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = Image.fromarray(frame)
   
    start = time.time()
    #results = model.DetectWithImage(frame, threshold=args["confidence"], kepp_aspect_ratio=True, relative_coord=False)
    results = model(frame)
    end = time.time()
   
    for r in results:
        box = r.bounding_box.flatten().astype("int")
        (startX, startY, endX, endY) = box
        label = labels[r.label_id]
       
        cv2.rectangle(ori, (startX, startY), (endX, endY), (0, 255, 0), 2)
        y = startY - 15 if startY - 15 > 15 else startY + 15
        test = "{}: {:.2f}%".format(label, r.score * 100)
        cv2.putText(ori, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imshow("Frame", ori)
    #cv2.imwrite("/home/pi/video/test.jpeg", ori)
    key = cv2.waitKey(1) & 0xFF
    #if key == ord("q"):
    #    break

    cv2.waitKey(1)

   
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
