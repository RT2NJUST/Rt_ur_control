#!/bin/bash
set -e

sudo apt-get update
sudo apt-get install zsh -y
sh -c "$(wget https://gitee.com/Devkings/oh_my_zsh_install/raw/master/install.sh -O -)"
sudo chsh -s /bin/zsh $USER

sudo apt install ros-humble-visualization-msgs -y
sudo apt install ros-humble-geometry-msgs -y