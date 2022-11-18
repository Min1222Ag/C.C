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

import socket
import rclpy
from rclpy.node import Node

from std_msgs.msg import String


class locationPublisher(Node):

    def __init__(self, host, port=6000, buf_size=4096):
        super().__init__('location_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(host, port)
        s.listen()
        self.conn, self.addr = s.accept()
        with self.conn:
            print("Connected by {}".format(self.addr))

    def timer_callback(self):
        with self.conn:
            data = self.conn.recv(self.buf_size)
            self.conn.sendall(data)
            with open(str(self.i))+".txt", "wb") as f:
                msg = String()
                msg.data = 'Hello World: %d' % self.i
                self.publisher_.publish(msg)
                self.get_logger().info('Publishing: "%s"' % msg.data)
                f.write(data)
            self.i += 1

def main(args=None):
    rclpy.init(args=args)

    location_publisher = locationPublisher()

    rclpy.spin(location_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    location_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
