#!/usr/bin/env python2.7
# Import ROS libraries and messages
import rclpy
from sensor_msgs.msg import Image

# Import OpenCV libraries and tools
import cv2
from cv_bridge import CvBridge, CvBridgeError

# Print "Hello!" to terminal
print("Hello!")


# Print "Hello ROS!" to the Terminal and to a ROS Log file located in ~/.ros/log/loghash/*.log
#rclpy.loginfo("Hello ROS!")

# Initialize the CvBridge class
bridge = CvBridge()

# Define a function to show the image in an OpenCV Window
def show_image(img):
  cv2.imshow("Image Window", img)
  cv2.waitKey(3)

# Define a callback for the Image message
def image_callback(img_msg):
  # log some info about the image topic
  rclpy.loginfo(img_msg.header)

  # Try to convert the ROS Image message to a CV2 Image
  try:
	  cv_image = bridge.imgmsg_to_cv2(img_msg, "passthrough")
  #except CvBridgeError, e:
  #	  print("dd")
  	  #rclpy.logerr("CvBridge Error: {0}".format(e))

  # Flip the image 90deg
  #cv_image = cv2.transpose(cv_image)
  #cv_image = cv2.flip(cv_image,1)

  # Show the converted image
  # show_image(cv_image)

# Initialize the ROS Node named 'opencv_example', allow multiple nodes to be run with this name
#rclpy.init_node('opencv_example', anonymous=True)
rclpy.init(args=args)
g_node = rclpy.create_node('camera_subscriber')

# Initalize a subscriber to the "/camera/rgb/image_raw" topic with the function "image_callback" as a callback
subscription = g_node.create_subscription(Image, "/image_raw", image_callback, 1000)
subscription


# Initialize an OpenCV Window named "Image Window"
cv2.namedWindow("Image Window", 1)

# Loop to keep the program from shutting down unless ROS is shut down, or CTRL+C is pressed
while rclpy.ok():
  rclpy.spin(g_node)
  
g_node.destroy_node()
rclpy.shutdown()
