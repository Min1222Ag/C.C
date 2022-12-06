import time
import socket
import rclpy
from rclpy.node import Node

from std_msgs.msg import String

HOST = socket.gethostbyname(socket.gethostname())
PORT = 6000
STORE_DIR = "/home/pi/C.C/test/PathSetting/path_info/"
PATH_FILE = "path.json"

class locationPublisher(Node):

    def __init__(self, socket, buf_size=4096, store_dir=STORE_DIR):
        super().__init__('location_publisher')
        self.publisher_ = self.create_publisher(String, 'location', 100)

        self.i = 0
        self.store_dir = store_dir
        self.buf_size = buf_size

        socket.settimeout(3)
        self.socket = socket
        self.socket.listen()

        timer_period = 0.01  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):

        msg = String()
        msg.data = 'callback [%d]' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        print("inner timer_callback")

        try:
            conn, addr = self.socket.accept()
            self.conn = conn
            data = self.conn.recv(self.buf_size)
            b_num = len(data)
            with self.conn:
                with open(self.store_dir + PATH_FILE, "wb") as f:
                    print("inner with open file")
                    f.write(data)
                    print("succeed in writing data!")

            print("{}: {} bytes received.".format(self.i, b_num))
        
        except socket.timeout:
            print("timeout {}".format(self.i))

        self.i += 1


def main(args=None):
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind((HOST, PORT))

    rclpy.init(args=args)

    location_publisher = locationPublisher(tcp_socket)

    rclpy.spin(location_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically

    location_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
