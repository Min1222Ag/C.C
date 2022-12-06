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

import motor_control    # for stopping two motors
import gps_tracking

import obstacles_detection
import obstacles_detect_node

import os
import json

RECEIVED_FILE = "home/pi/C.C/test/PathSetting/path_info/coordinates.json"
SUBGOALS_FILE = "home/pi/C.C/test/PathSetting/path_info/on_going.json"
RENDEZVOUS = 10
RIGHT_THRESHOLD = 10
LEFT_THRESHOLD = 10
PINS = [18, 23, 24, 16, 20, 21]
DUMPSTER_LOCATION = (0, 0) # a GPS coordinate of dumpster

# motorSubscriber : subscribe '/Stop' topic from 'obstacles_detection' file
class motorSubscriber(Node):

    def __init__(self):
        super().__init__('motor_subscriber') # node name : motor_subscriber
        self.subscription = self.create_subscription(
            Stop,       # topic type : Stop
            'Stop',     # topic name : Stop
            self.running,    # callback function
            200)      # queue size : 200
        
        self.subscription  # prevent unused variable warning
        self.phase = 1

        self.curr = 0

        self.gps_tracker = gps_tracking.GPSTracking()
        self.motor_controller = motor_control.motorControl(PINS) # motor_control.py > Class motorControl
        print("subscription")

    def running(self, msg=None):
        print("now in the phase {}".format(self.phase))

        # PHASE 1
        if self.phase == 1:
            # file existing?
            if not os.path.exists(RECIEVED_FILE):
                return # if does not, wait

            # if does read json
            with open(RECIEVED_FILE, 'r') as f:
                coord_data = json.load(f)

            self.dumpster_coord = coord_data["dumpster_coordinate"]

            start_lat = coord_data["start_coordinate"]["latitude"]
            start_lon = coord_data["start_coordinate"]["longitude"]

            dest_lat = coord_data["end_coordinate"]["latitude"]
            dest_lon = coord_data["end_coordinate"]["longitude"]

            gap = coord_data["meter"]

            self.gps_tracker.subgoals(start_lat, start_lon, end_lat, end_lon, gap)
            
            if not os.path.exists(SUBGOALS_FILE):
                return # if does not, wait

            with open(SUBGOALS_FILE, 'r') as f:
                self.subgoals = json.load(f)

            self.phase = 2
        
        # check signal or trashbin
        if msg != None:
            print("got message from detection unit")
            if msg.stop:
                turn_left, turn_right = self.get_signal(msg)
                
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
            dest_coord = self.subgoals["latitude"][str(self.curr)], self.subgoals["longitude"][str(self.curr)]
            arriving = self.driving(dest_coord)
            
            if arriving:
                # if it arrived at the current destination, set the next
                self.curr += 1
                if self.curr == len(self.subgoals["latitude"].keys()):
                    self.phase = 3

        # PHASE 3
        if self.phase == 3:
        # after pass all subgoals go to dumpster
            arriving = self.driving(self.dumpster_coord)
            if arriving:
                self.phase = 1
                self.curr = 0
                os.remove(SUBGOALS_FILE)
        
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

    # check if the trash bin is full or not
    def check_full(self):
        print("trash bin is full")
        # will be updated

def main(args=None):
    rclpy.init(args=args)
    motor_speed = obstacles_detect_node.lidarDetect() # obstacles_detection.py > Class lidarDetect
    # motor_speed.decision_callback() # never mind

    motor_subscriber = motorSubscriber()

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
