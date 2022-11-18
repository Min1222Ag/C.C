import rclpy
from rclpy.node import Node

from std_msgs.msg import String

class locationSubscriber(Node):

    def __init__(self):
        super().__init__('location_subscriber')
        self.subscription = self.create_subsciption(
                String,
                'location',
                self.listener_callback,
                10)
        self.subscription # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('I heard: {}'.format(msg.data))

def main(args=None):
    rclpy.init(args=args)

    location_subscriber = locationSubscriber()

    rclpy.spin(location_subscriber)

    location_subscriber.destroy_node()
    
    rclpy.shotdown()

if __name__ == '__main__':
    main()
