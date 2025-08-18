#!/bin/zsh

cd /workspaces/ur_control/rt_ws

source /opt/ros/humble/setup.zsh

rosdep update && rosdep install --ignore-src --from-paths . -y

colcon build

source /workspaces/ur_control/rt_ws/install/setup.zsh
