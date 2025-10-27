FROM osrf/ros:humble-desktop-full

# 定义用户和用户组
ARG USERNAME=yc-dlan
ARG USER_UID=1000
ARG USER_GID=$USER_UID

#安装相关包
ARG ROS_DISTRO=humble

WORKDIR /home/${USERNAME}/Rt_ur_control/packages

# 合并所有apt-get操作并清理缓存
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    sudo nautilus wget software-properties-common curl \
    gcc git zip unzip htop libgl1 libglib2.0-0 gnupg libsm6 && \
    # 添加fish仓库并安装
    add-apt-repository ppa:fish-shell/release-3 -y && \
    apt-get update && \
    apt-get install -y fish fzf && \
    # 清理
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 创建用户组和用户
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    # 配置环境变量
    && echo "$USERNAME:'" | chpasswd \
    # 允许用户使用 sudo
    && usermod -aG sudo $USERNAME \
    && echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers \
    && echo 'source /opt/ros/humble/setup.bash' >> /home/$USERNAME/.bashrc \
    && chown -R $USERNAME:$USERNAME /home/$USERNAME \
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
    ros-humble-moveit* \
    #cmake相关依赖
    ros-humble-ament-cmake \
    ros-humble-ament-cmake-cpplint \
    ros-humble-ament-cmake-clang-format \
    ros-humble-ament-cmake-gtest \
    #视觉处理包
    ros-humble-vision-opencv \
    #深度相机驱动
    ros-humble-realsense2-camera \
    #UR机械臂驱动
    ros-humble-ur \
    #gazebo
    gazebo \
    #ros2 control
    ros-humble-ros2-control \
    ros-humble-ros2-controllers \
    ros-humble-moveit-servo \
    ros-humble-gazebo-plugins \
    ros-humble-gazebo-ros \
    #image dependency
    ros-humble-image-pipeline \
    ros-humble-compressed-image-transport \
    ros-humble-compressed-depth-image-transport \
    ros-humble-vision-msgs 

# 安装CopperliaSim依赖
RUN apt-get update && apt-get install -y \
    xsltproc

RUN pip3 install xmlschema lxml

# 安装gazebo相关依赖
RUN apt-get update && apt-get install -y \
    lsb-release \
    gnupg \
    ignition-fortress && \
    rm -rf /var/lib/apt/lists/*

# 添加OSRF仓库的GPG密钥
RUN curl https://packages.osrfoundation.org/gazebo.gpg --output /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg

# 添加OSRF仓库到源列表
RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null

# 安装colcon构建系统及mixin配置
RUN pip3 install -U colcon-common-extensions \
    && apt-get install -y python3-colcon-mixin 

#拉取开源镜像
#RUN mkdir -p /home/${USERNAME}/packages/src && \
#    cd /home/${USERNAME}/packages/src && \
#    git clone -b humble https://github.com/UniversalRobots/Universal_Robots_ROS2_Description.git && \
#    git clone -b humble https://github.com/UniversalRobots/Universal_Robots_ROS2_Gazebo_Simulation.git && \
#    git clone -b humble https://github.com/UniversalRobots/Universal_Robots_ROS2_Driver.git 
#    #cd .. && \
#    #colcon build --symlink-install

#切回yc-dlan
USER yc-dlan

# 安装fish插件（切换到普通用户）
RUN curl -L https://github.com/oh-my-fish/oh-my-fish/raw/master/bin/install | sudo tee install_omf > /dev/null && \
    fish install_omf --noninteractive && \
    fish -c "omf install bass" && \
    sudo rm install_omf 

# 复制fish配置
COPY packages/fish /home/${USERNAME}/.config/fish

WORKDIR /home/${USERNAME}

CMD [ "/bin/bash" ]