#!/bin/bash

workspace=$(pwd)

source ~/.bashrc

# CAN
gnome-terminal -t "can1" -x sudo bash -c "cd ${workspace};cd A5/ARX_CAN ; ./arx_can1; exec bash;"
gnome-terminal -t "can3" -x sudo bash -c "cd ${workspace};cd A5/ARX_CAN ; ./arx_can3; exec bash;"
gnome-terminal -t "can3" -x sudo bash -c "cd ${workspace};cd A5/ARX_CAN ; ./arx_can0; exec bash;"
gnome-terminal -t "can3" -x sudo bash -c "cd ${workspace};cd A5/ARX_CAN ; ./arx_can5; exec bash;"
gnome-terminal -t "can3" -x sudo bash -c "cd ${workspace};cd A5/ARX_CAN ; ./arx_can6; exec bash;"

sleep 1

# robot
gnome-terminal -t "A5" -x  bash -c "cd ${workspace}; cd A5;  source setup.sh && python3 test_dual_arm.py; exec bash;"
sleep 0.1

gnome-terminal -t "LIFT" -x  bash -c "cd ${workspace}; cd LIFT-mini;  source setup.sh && python3 joystick_control.py; exec bash;"