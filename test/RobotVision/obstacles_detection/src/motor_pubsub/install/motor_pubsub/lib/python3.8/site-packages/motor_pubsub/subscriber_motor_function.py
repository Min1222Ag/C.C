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

import rclpy
from rclpy.node import Node

# use custom messages '/Stop' 
from interfaces.msg import Stop

#############################import################################
# import motorControl.py for stop two motor
import motorControl
import obstacles_detection

stop_function = motorControl.MotorControl() # motorControl.py > Class MotorControl 
motor_speed = obstacles_detection.lidarDetect() # ovstacles_detection.py > Class lidarDetect
# motor_speed.decision_callback() # never mind

###################################################################

# motorSubscriber : subscribe '/Stop' topic from 'obstacles_detection' file
class motorSubscriber(Node):

    def __init__(self):
        super().__init__('motor_subscriber') # motor name : motor_subscriber
        self.subscription = self.create_subscription(
            Stop,       # message type : Stop
            'Stop',     # topic name : Stop
            self.get_signal,
            100)      # queue size : 100
        self.subscription  # prevent unused variable warning
        print("kk")

    # get signal from a LiDAR and proximity sensor
    def get_signal(self, msg):
        print("ss")
        print(msg)
        ###########################################################
        if msg.stop = 0: # Execute motorControl.py > MotorControl Class > def stop
            stop_function.stop() # Class MotorControl > def stop()            

        msg.lspeed
        msg.rspeed
        ###########################################################
        self.get_logger().info('I heard: "%d"' % msg.stop)


def main(args=None):
    rclpy.init(args=args)
    print("1")

    motor_subscriber = motorSubscriber()
    print("2")

    rclpy.spin(motor_subscriber)
    print("3")

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    motor_subscriber.destroy_node()
    rclpy.shutdown()
    print("sss")

if __name__ == '__main__':
    main()
