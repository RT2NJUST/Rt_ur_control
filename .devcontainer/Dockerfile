FROM osrf/ros:humble-desktop-full

# 定义用户和用户组
ARG USERNAME=yc-dlan
ARG USER_UID=1000
ARG USER_GID=$USER_UID

#安装相关包
ARG ROS_DISTRO=humble

WORKDIR /home/${USERNAME}/Rt_ur_control/packages

# 创建用户组和用户
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    # 配置环境变量
    && echo "$USERNAME:'" | chpasswd \
    # 允许用户使用 sudo
    && usermod -aG sudo $USERNAME \
    && echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers \
    && echo 'source /opt/ros/humble/setup.bash' >> /home/$USERNAME/.bashrc \
    # 使新用户的 `.bashrc` 文件生效
    && chown $USERNAME:$USERNAME /home/$USERNAME/.bashrc

#转换为root用户执行安装
USER root

# 安装基础依赖
RUN apt-get update \
    && apt-get install -y \
    net-tools \
    nautilus \
    bash-completion \
    clangd \
    git \
    gedit \
    gdb \
    build-essential \
    cmake \
    python3-colcon-common-extensions \
    python3-flake8 \
    python3-rosdep \
    python3-setuptools \
    python3-vcstool \
    wget \
    python3-pip \
    # 添加ROS2编译工具
    ros-dev-tools \
    # 安装MoveIt2核心依赖
    ros-humble-moveit-visual-tools \
    ros-humble-xacro 

# 安装必要的 ROS 包
RUN apt-get update && apt-get install -y \
    ros-humble-desktop \
    ros-humble-moveit \
    #视觉处理包
    ros-humble-vision-opencv \
    #深度相机驱动
    ros-humble-realsense2-camera \
    #UR机械臂驱动
    ros-humble-ur
    
# 安装colcon构建系统及mixin配置
RUN pip3 install -U colcon-common-extensions \
    && apt-get install -y python3-colcon-mixin 

# 克隆并编译moveit2_tutorials
RUN mkdir -p /home/${USERNAME}/Rt_ur_control/packages/ros_ws/src && \
    cd /home/${USERNAME}/Rt_ur_control/packages/ros_ws/src && \
    git clone -b $ROS_DISTRO https://github.com/moveit/moveit2_tutorials.git && \
    vcs import --recursive < moveit2_tutorials/moveit2_tutorials.repos && \
    cd .. && \
    sudo apt remove -y ros-$ROS_DISTRO-moveit* && \
    sudo apt update && \
    rosdep install -r --from-paths . --ignore-src --rosdistro $ROS_DISTRO -y && \
    bash -c "source /opt/ros/$ROS_DISTRO/setup.bash && \
    colcon build --symlink-install --mixin release compile-commands --executor sequential --parallel-workers 2"

# 克隆并编译Universal_Robots_ROS2_Driver
RUN cd /home/${USERNAME}/Rt_ur_control/packages/ros_ws/src && \
    git clone -b $ROS_DISTRO https://github.com/UniversalRobots/Universal_Robots_ROS2_Driver.git && \
    vcs import --skip-existing --input Universal_Robots_ROS2_Driver/Universal_Robots_ROS2_Driver-not-released.${ROS_DISTRO}.repos && \
    rosdep update && \
    rosdep install --ignore-src --from-paths . -y && \
    cd .. && \
    bash -c "source /opt/ros/$ROS_DISTRO/setup.bash && \
    colcon build --cmake-args -DCMAKE_BUILD_TYPE=Release"

#切回yc-dlan
USER yc-dlan

WORKDIR /home/${USERNAME}

CMD [ "/bin/bash" ]