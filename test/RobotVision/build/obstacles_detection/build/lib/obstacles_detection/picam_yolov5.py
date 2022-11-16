#!/usr/bin/env python
# coding:utf-8

import rclpy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge, CvBridgeError

print
import numpy as np

cv2.imshow("Image Window", img)
cv2.waitKey(3)
cv2.namedWindow("Image Window", 1)
