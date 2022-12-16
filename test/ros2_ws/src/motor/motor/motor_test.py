# test code independent of the detection publisher
import motor_control # for controlling two motors
import gps_tracking # for following the path
import proximity # for detecting obstacles taken at the driving unit level

import os
import json

RECEIVED_FILE = os.path.join(os.getcwd()+"/PathSetting/path_info/coordinates.json") # received coordinates information
SUBGOALS_FILE = os.path.join(os.getcwd()+"/PathSetting/path_info/on_going.json") 

RENDEZVOUS = 10 # approaching to a subgoal

# angle thresholds between heading and bearing
RIGHT_THRESHOLD = 10
LEFT_THRESHOLD = 10

MAGINOT_LINE = 10 # approaching obstacle by the centimeter
RELAY_PINS = [18, 23, 24, 16, 20, 21, 27] # pins for controlling motors
PROXIMITY_PINS = {"front": [10, 9], "back": [6, 13], "inner": [19, 26]} # pins for proximity sensors
CAPACITY = 10
# motorSubscriber : subscribe '/Stop' topic from 'obstacles_detection' file
class motorTest:

    def __init__(self):
        self.phase = 1 # phase indicator

        self.curr = 0 # current subgoals index

        self.gps_tracker = gps_tracking.GPSTracking() # module for subgoal tracking
        self.proximities = {"front": proximity.Proximity(PROXIMITY_PINS["front"][0], PROXIMITY_PINS["front"][1], "front"),
                            "back": proximity.Proximity(PROXIMITY_PINS["back"][0], PROXIMITY_PINS["back"][1], "back"),
                            "inner": proximity.Proximity(PROXIMITY_PINS["inner"][0], PROXIMITY_PINS["inner"][1], "inner")}
        # 3 proximity sensors for detecting obstacels and height of the collected trash

        self.motor_controller = motor_control.motorControl(RELAY_PINS) # module for motor controlling
        print("subscription")

    def running(self, msg=None):
        print("now in the phase {}".format(self.phase))

        # PHASE 1: getting subgoals from files
        if self.phase == 1:
            # file existing?
            if not os.path.exists(RECEIVED_FILE):
                print("not existed")
                return # if does not, wait

            # if does read json
            with open(RECEIVED_FILE, 'r') as f:
                coord_data = json.load(f)

            # get coordinates required
            self.dumpster_coord = coord_data["dumpster_coordinate"]
            start_lat = coord_data["start_coordinate"]["latitude"]
            start_lon = coord_data["start_coordinate"]["longitude"]
            end_lat = coord_data["end_coordinate"]["latitude"]
            end_lon = coord_data["end_coordinate"]["longitude"]
            gap = coord_data["meter"] # gap

            self.gps_tracker.subgoals(start_lat, start_lon, end_lat, end_lon, gap) # generate subgoals from start coordinate to end coordinate
            
            # file existing?
            if not os.path.exists(SUBGOALS_FILE):
                return # if does not, wait

            # if does read json
            with open(SUBGOALS_FILE, 'r') as f:
                self.subgoals = json.load(f)

            self.phase = 2 # ready to move on next phase
        
        # check signal from detection unit
        if msg != None:
            print("got message from detection unit")
            if msg.stop: # if detection unit messages to stop
                print(msg)
                # decision of direction to avoid
                turn_left, turn_right = self.get_signal(msg)
                if turn_left:
                    self.motor_controller.left_ahead()
                elif turn_right:
                    self.motor_controller.right_ahead()
                else:
                    self.motor_controller.stop()
                return # end of callback function

        # check trash bin is full
        if self.check_full():
            self.throwing = True # throwing mode
            self.phase = 3 # go to dumpster phase
            return # end of callback function

        # check if there are obstacles
        if self.check_obstacle(): # avoid
            return # end of callback function

        # PHASE 2: driving to the certain subgoal
        if self.phase == 2:
            # set current destination location
            dest_coord = self.subgoals["latitude"][str(self.curr)], self.subgoals["longitude"][str(self.curr)]
            arriving = self.driving(dest_coord)
            
            if arriving:
                # if it arrived at the current destination, set the next
                self.curr += 1
                if self.curr == len(self.subgoals["latitude"].keys()):
                    self.phase = 3 # if the destination was last one, ready to move on next phase

        # PHASE 3: driving to the dumpster
        if self.phase == 3:
        # after pass all subgoals go to dumpster
            arriving = self.driving(self.dumpster_coord)
            if arriving: # if arrived at the destination
                if self.throwing: # if there are left subgoals
                    self.throwing = False # go back to cleaning mode dumpster
                    self.phase = 2
                else: # if the cleaning end
                    self.phase = 1 # go back to first phase
                    # reset
                    self.curr = 0
                    os.remove(SUBGOALS_FILE)

    def driving(self, dest_coord):
        # driving to certain destination coordinate

        curr_coord = self.gps_tracker.readGPS() # read current location
        if curr_coord == None:
            return False # arriving is not true

        print("driving at {}".format(curr_coord))
        # set current coordinate and destination coordinate
        dest_lat, dest_lon = dest_coord[0], dest_coord[1]
        curr_lat, curr_lon = curr_coord[0], curr_coord[1]

        if self.phase == 2: # if in cleaning step
            self.motor_controller.broom_run() # broom run
        if self.phase == 3: # if in throwing step
            self.motor_controller.broom_stop() # broom stop

        if self.gps_tracker.distance(curr_lat, curr_lon, dest_lat, dest_lon) < RENDEZVOUS:
            # if it arrived at the current destination
            return True # arriving is true

        else:
            bearing = self.gps_tracker.bearing(curr_lat, curr_lon, dest_lat, dest_lon)
            # calculate bearing
                    
            if bearing > LEFT_THRESHOLD:
                # if it is heading left, turn right little bit
                self.motor_controller.right_ahead()

            elif bearing < RIGHT_THRESHOLD:
                # if it is heading right, turn left little bit
                self.motor_controller.left_ahead()

            else:
                # if it is heading the intended direction in tolerable range, go ahead
                self.motor_controller.ahead()

            return False # arriving is not true

    # get signal from a LiDAR and proximity sensor
    def get_signal(self, msg):
        print("msg: {}".format(msg))
        return msg.lspeed, msg.rspeed # decide which side to avoid

    # check if the trash bin is full or not
    def check_full(self):
        print("check if trash bin is full")
        return self.proximities["inner"].measure() < CAPACITY # based on height mesured via proximity sensor

    # check the obstacles
    def check_obstacle(self):
        print("check obstacles with proximity sensor")
        # if obstacle in the front
        if self.proximities["front"].measure() < MAGINOT_LINE:
            # if obstacle in the back
            if self.proximities["back"].measure() < MAGINOT_LINE:
                self.motor_controller.stop()
            else: # if no obstacle in the back
                self.motor_controller.back() # go back
            self.motor_controller.broom_stop() # broom stop
            return True # obstacle avoiding phase
        else: # no obstacle
            self.motor_controller.broom_run() # broom run
            return False

def main(args=None):
    motor_test = motorTest()

    while(True):
        motor_test.running()
if __name__ == '__main__':
    main()
