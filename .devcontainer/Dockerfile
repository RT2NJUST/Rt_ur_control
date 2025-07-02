FROM osrf/ros:humble-desktop-full

# 定义用户和用户组
ARG USERNAME=yc-dlan
ARG USER_UID=1000
ARG USER_GID=$USER_UID

ENV DEBIAN_FRONTEND=noninteractive

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
    
# 安装colcon构建系统
RUN pip3 install -U colcon-common-extensions

#切回yc-dlan
USER yc-dlan

WORKDIR /home/${USERNAME}

CMD [ "/bin/bash" ]