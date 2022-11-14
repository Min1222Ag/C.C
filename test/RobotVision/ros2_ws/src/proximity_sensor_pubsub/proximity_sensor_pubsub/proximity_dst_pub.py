from rclpy.node import Node

from sensor_msgs.msg import Range

import RPi.GPIO as GPIO
import time

class proximityDetect(Node):
    def __init__(self):
        super().__init__('proximity_node') # node name
        self.distance_publisher = self.create_publisher(Range, 'Proximity', 100) # message type : , topic name: proximity
        timer_period = 0.5  # seconds
        self.proximity_timer = self.create_timer(timer_period, self.publish_distance)

    # get the log information
    def publish_distance(self):
        msg=Range()
        msg.data=self.distacne
        self.distance_publisher.publish(msg)
        self.get_logger().info('Publishing (distance) : "%f"' %msg.data)

    # set up the proximity sensor
    def proximity_sensor(self):
        try:
            GPIO.setmode(GPIO.BCM)

            PIN_TRIGGER = 23
            PIN_ECHO = 24

            GPIO.setup(PIN_TRIGGER, GPIO.OUT)
            GPIO.setup(PIN_ECHO, GPIO.IN)

            GPIO.output(PIN_TRIGGER, GPIO.LOW)

            # print "Waiting for sensor to settle"

            time.sleep(2)

            # print "Calculating distance"

            GPIO.output(PIN_TRIGGER, GPIO.HIGH)

            time.sleep(0.00001)

            GPIO.output(PIN_TRIGGER, GPIO.LOW)

            while GPIO.input(PIN_ECHO) == 0:
                self.pulse_start_time = time.time()
            while GPIO.input(PIN_ECHO) == 1:
                self.pulse_end_time = time.time()

            self.pulse_duration = self.pulse_end_time - self.pulse_start_time
            self.distance = round(self.pulse_duration * 17150, 2)
            print("Distance:", self.distance, "cm")

        finally:
            GPIO.cleanup()


def main(args=None):
    rclpy.init(args=args)
    proximity_node = proximityDetect()
    rclpy.spin(proximity_node)
    rclpy.shutdown()

if __name__=='__main__':
    main()
