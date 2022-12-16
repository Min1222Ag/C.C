#!/bin/bash

CURR=`pwd`
SRCDIR="${CURR}/ros2_ws/src/"
INTERFACEDIR="${CURR}/ros2_ws/src/interfaces/"
DETECTIONDIR="${CURR}/ros2_ws/src/obstacles_detection/obstacles_detection/"
MOTORDIR1="${CURR}/ros2_ws/src/motor/motor/"
MOTORDIR2="${CURR}/ros2_ws/src/motor/"

export PYTHONPATH="${PYTHONPATH}:${SRCDIR}:${INTERFACEDIR}:${DETECTIONDIR}:${MOTORDIR1}:${MOTORDIR2}"