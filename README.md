# Rt_ur_control
## 本项目采用docker容器开发，将一些相关的软件包安放在容器内部文件夹，简化了文件的架构。 
## （This project is developed using Docker containers, and some related software packages are placed in the internal folder of the container, simplifying the file architecture.）

### 三个官方仓库文档
- Universal_Robots_ROS2_Description (https://github.com/UniversalRobots/Universal_Robots_ROS2_Description.git)  
- Universal_Robots_ROS2_Driver (https://github.com/UniversalRobots/Universal_Robots_ROS2_Driver.git)
- Universal_Robots_ROS2_Gazebo_Simulation (https://github.com/UniversalRobots/Universal_Robots_ROS2_Gazobo_Simulation.git)

### 本地化功能包(ur_driver)
- `gazebo_driver` - 驱动gazebo的包，对应上面的第三个源码 

- `gazebo_ros` - 官方gazebo包，主要是替换场景 

- `moveit_driver` - moveit驱动包，主要修改参数文件 

- `robot_driver` - 机器人实体驱动包，目前跑仿真，基本用不上 

- `ur5_description` - 机器人的描述，urdf和srdf文件，以及相关参数文件

### 说明
上述功能包的launch文件名字基本上没有改变，只是改变了功能包名称，主要是对将夹爪模型添加到了机器人的模型中。

### BUG

1. **Gazobo无响应**

2. **模型没有同步加载，已添加ws_simulation.world的场景**

3. **unable to locate package ros-humble-gazebo-ros2-control**

4. **Could not contact service /controller_manager/list_controllers**
### 使用

```bash
$ git clone -b Dlan_servo git@github.com:RT2NJUST/Rt_ur_control.git

$ cd .devcontainer

$ docker compose build

$ docker compose up -d

$ docker exec -it Rt_ur_control bash

$ colcon build

$ source install/setup.bash

$ ros2 launch gazebo_driver ur_sim_control.launch.py
$ ros2 launch gazebo_driver ur_sim_moveit.launch.py
```