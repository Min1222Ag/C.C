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
import motor_control    # for stopping two motors
import gps_tracking

import obstacles_detection
import obstacles_detect_node

import os
import json

SUBGOALS_FILE = "home/pi/C.C/test/PathSetting/path_info/path_info.json"
RENDEZVOUS = 10
RIGHT_THRESHOLD = 10
LEFT_THRESHOLD = 10
PINS = [18, 23, 24, 16, 20, 21]
DUMPSTER_LOCATION = (0, 0) # a GPS coordinate of dumpster

# motorSubscriber : subscribe '/Stop' topic from 'obstacles_detection' file
class motorSubscriber(Node):

    def __init__(self):
        super().__init__('motor_subscriber') # motor name : motor_subscriber
        self.subscription = self.create_subscription(
            Stop,       # message type : Stop
            'Stop',     # topic name : Stop
            self.running,
            200)      # queue size : 200
        
        self.subscription  # prevent unused variable warning
        self.phase = 1

        self.subgoals = []
        self.curr = 0

        self.gps_tracker = gps_tracking.GPSTracking()
        self.motor_controller = motor_control.motorControl(PINS) # motor_control.py > Class motorControl
        print("subscription")

    def running(self, msg=None):
        print("now in the phase {}".format(self.phase))

        # PHASE 1
        if self.phase == 1:
            # file existing?
            if not os.path.exists(SUBGOALS_FILE):
                return # if does not, wait

            # if does read json
            with open(SUBGOALS_FILE, 'r') as f:
                path_data = json.load(f)

            # check validity of the file
            if len(path_data["subgoals"]) != path_data["number"] or len(path_data["subgoals"]) == 0:
                print(len(path_data["subgoals"]), path_data["number"])
                return # error

            self.subgoals = path_data["subgoals"]
            self.phase = 2
        
        # check signal or trashbin
        if msg != None:
            print("got message from detection unit")
            turn_left, turn_right = self.get_signal(msg)

            if msg.stop:
                if turn_left:
                    self.motor_controller.left()
                elif turn_right:
                    self.motor_controller.right()
                else:
                    self.motor_controller.stop()
                return

        # PHASE 2
        if self.phase == 2:
            # set current destination location
            dest_coord = self.subgoals[self.curr]["latitude"], self.subgoals[self.curr]["longitude"]
            arriving = self.driving(dest_coord)
            
            if arriving:
                # if it arrived at the current destination, set the next
                self.curr += 1
                if self.curr == len(self.subgoals):
                    self.phase = 3

        # PHASE 3
        if self.phase == 3:
        # after pass all subgoals go to dumpster
            arriving = self.driving(DUMPSTER_LOCATION)
            if arriving:
                self.phase = 1
                self.curr = 0
        
    def driving(self, dest_coord):
        curr_coord = self.gps_tracker.readGPS() # read current location
        if curr_coord == None:
            return False

        print("driving at {}".format(curr_coord))
        dest_lat, dest_lon = dest_coord[0], dest_coord[1]
        curr_lat, curr_lon = curr_coord[0], curr_coord[1]

        if self.gps_tracker.distance(curr_lat, curr_lon, dest_lat, dest_lon) < RENDEZVOUS:
            # if it arrived at the current destination
            return True

        else:
            bearing = self.gps_tracker.bearing(curr_lat, curr_lon, dest_lat, dest_lon)
            # calculate bearing
                    
            if bearing > LEFT_THRESHOLD:
                # if it is heading left, turn right little bit
                self.motor_controller.right()

            elif bearing < RIGHT_THRESHOLD:
                # if it is heading right, turn left little bit
                self.motor_controller.left()

            else:
                # if it is heading the intended direction in tolerable range, go ahead
                self.motor_controller.ahead()

            return False

    # get signal from a LiDAR and proximity sensor
    def get_signal(self, msg):
        print("msg: {}".format(msg))
        return msg.lspeed, msg.rspeed

    def check_full(self):
        print("trash bin is full")
        # will be updated

def main(args=None):
    rclpy.init(args=args)
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
