#!/bin/zsh

source /opt/ros/humble/setup.zsh

ros2 daemon start

source /workspaces/ur_control/rt_ws/install/setup.zsh

ros2 launch ur5_simulator view_ur5_camera_gripper.launch.py