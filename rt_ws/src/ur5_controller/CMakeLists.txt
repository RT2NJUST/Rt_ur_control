cmake_minimum_required(VERSION 3.8)
project(ur5_controller)

if (CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(moveit_ros_planning_interface REQUIRED)
find_package(geometry_msgs REQUIRED)

add_executable(ur5_controller_node src/ur5_controller_node.cpp)

ament_target_dependencies(ur5_controller_node
  rclcpp
  moveit_ros_planning_interface
  geometry_msgs
)

install(TARGETS
  ur5_controller_node
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()