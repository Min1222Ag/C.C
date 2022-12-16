#!/bin/bash

cd PathSetting
pwd
rm path_info/coordinates.json
rm path_info/on_going.json
cd path_ws
pwd
colcon build
. install/setup.bash
ros2 run path_package path_receiver &
cd ../../ros2_ws
pwd
colcon build
. install/setup.bash
ros2 run motor listener
