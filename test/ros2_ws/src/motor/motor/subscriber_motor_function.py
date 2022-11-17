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
# import motor_control.py for stopping two motors


###################################################################
class motorSubscriber(Node):

    def __init__(self):
        super().__init__('motor_subscriber') # motor name : motor_subscriber
        self.subscription = self.create_subscription(
        self.subscription  # prevent unused variable warning
        print("get_signal operated")
        print(msg)
        ###########################################################
            stop_function.stop() # Class motorControl > def stop()

        #msg.lspeed
        #msg.rspeed
        ###########################################################
        #self.get_logger().info('I heard: "%d"' % msg.stop)
        print(msg.stop)

def main(args=None):
    rclpy.init(args=args)
    stop_function = motor_control.motorControl([1, 2, 3, 4, 5, 6]) # motor_control.py > Class motorControl
    motor_speed = obstacles_detect_node.lidarDetect() # obstacles_detection.py > Class lidarDetect
    # motor_speed.decision_callback() # never mind
    print("1")

    motor_subscriber = motorSubscriber()
    print("2")

    rclpy.spin(motor_subscriber)
    print("spin")

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    motor_subscriber.destroy_node()
    rclpy.shutdown()
    print("shutdown")

if __name__ == '__main__':
    main()
                                            
