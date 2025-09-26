FROM osrf/ros:noetic-desktop-full

# 定义用户和用户组
ARG USERNAME=yc-dlan
ARG USER_UID=1000
ARG USER_GID=$USER_UID
ARG ROS_DISTRO=noetic
ENV DEBIAN_FRONTEND=noninteractive

# 创建用户组和用户
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    # 配置密码
    && echo "$USERNAME:password" | chpasswd \
    # 允许用户使用 sudo
    && usermod -aG sudo $USERNAME \
    && echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers \
    # 配置 ROS 环境
    && echo "source /opt/ros/$ROS_DISTRO/setup.bash" >> /home/$USERNAME/.bashrc \
    # 使新用户的 `.bashrc` 文件生效
    && chown $USERNAME:$USERNAME /home/$USERNAME/.bashrc

# 安装基础依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
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
    ros-dev-tools \
    software-properties-common \
    curl \
    vim \
    nano \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 安装额外的开发工具
RUN add-apt-repository ppa:fish-shell/release-3 -y \
    && apt-get update \
    && apt-get install -y fish fzf \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 安装夹爪和ur机械臂相关功能包
RUN apt-get update && apt-get install -y \
    ros-noetic-soem \
    ros-noetic-moveit-core \
    ros-noetic-moveit-ros-planning \
    ros-noetic-moveit-ros-move-group \
    ros-noetic-moveit-planners-ompl \
    ros-noetic-moveit-ros-visualization \
    ros-noetic-moveit-simple-controller-manager \
    ros-noetic-joint-trajectory-controller \
    ros-noetic-industrial-robot-status-interface \
    ros-noetic-scaled-joint-trajectory-controller \
    ros-noetic-speed-scaling-interface \
    ros-noetic-speed-scaling-state-controller \
    ros-noetic-pass-through-controllers \
    ros-noetic-ur-client-library \
    ros-noetic-trac-ik-kinematics-plugin

WORKDIR /home/$USERNAME
USER $USERNAME

# 初始化 ROS
RUN rosdep update

# 设置默认命令
CMD ["/bin/bash"]