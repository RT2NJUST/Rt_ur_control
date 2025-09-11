from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    
    declared_arguments = [
        DeclareLaunchArgument(
            "ur_type",
            default_value="ur5",
            description="机械臂型号"
        )
        ,
        DeclareLaunchArgument(
            "robot_ip",
            default_value="192.168.1.102",
            description="UR机器人控制器IP地址"
        ),
        DeclareLaunchArgument(
            "use_fake_hardware",
            default_value="true",
            description="是否使用仿真模式"
        ),
        DeclareLaunchArgument(
            "launch_rviz",
            default_value="true",
            description="是否启动RViz"
        ),
        DeclareLaunchArgument(
            "launch_servo",
            default_value="true",
            description="是否启动servo控制"
        )
    ]

    return LaunchDescription(declared_arguments + [OpaqueFunction(function=launch_setup)])

def launch_setup(context, *args, **kwargs):

    gz_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare("ur_simulation_gazebo"),
                "launch/ur_sim_moveit.launch.py"
            ])
        ]),
        launch_arguments=[
            ("ur_type", LaunchConfiguration("ur_type")),
            ("robot_ip", LaunchConfiguration("robot_ip")),
            ("use_fake_hardware", LaunchConfiguration("use_fake_hardware")),
            ("launch_rviz", LaunchConfiguration("launch_rviz")),
            ("launch_servo", LaunchConfiguration("launch_servo"))  # 确保官方Servo节点启动
        ]
    )

    teleop_node = Node(
        package="teleop_driver",
        executable="logitech_control",
        name="logitech_control",
        output="screen"
    )

    joy_node = Node(
        package='joy',
        executable='joy_node',
        name='joy_node',
        parameters=[{
            'dev': '/dev/input/js0',  # 手柄设备路径
            'deadzone': 0.1,
            'autorepeat_rate': 20.0
        }]  
    )

    node_to_start = [teleop_node, gz_launch, joy_node]

    return node_to_start