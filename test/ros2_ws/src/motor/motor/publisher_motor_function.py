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

# used for message type
from std_msgs.msg import Bool

# motorPublisher : publish the messages about motor > 'motor_on' or 'motor_off' [Boolean]
class motorPublisher(Node):

    def __init__(self):
        super().__init__('motor_publisher') # node name : motor_publisher
        self.publisher_ = self.create_publisher(Bool, 'motor_on', 100) # topic type : Bool , topic name : motor_on , queue size: 100
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.motor_publish) # call self.motor_publish()


    def motor_publish(self):
        msg = Bool()
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%d"' % msg.data)



def main(args=None):
    rclpy.init(args=args)

    motor_publisher = motorPublisher()

    rclpy.spin(motor_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)

    motor_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
