from moveit_configs_utils import MoveItConfigsBuilder
from moveit_configs_utils.launches import generate_move_group_launch
from ament_index_python.packages import get_package_share_path
import xacro
import os

def generate_launch_description():
    # 构建MoveIt配置
    moveit_config = MoveItConfigsBuilder("ur5", package_name="ur5_moveit_config").to_moveit_configs()
    
    # 手动指定initial_positions.yaml路径（指向ur5_moveit_config的config目录）
    initial_positions_file = os.path.join(
        get_package_share_path("ur5_moveit_config"),
        "config",
        "initial_positions.yaml"
    )
    
    # 加载初始位置文件
    #moveit_config.robot_description.initial_positions = xacro.load_yaml(initial_positions_file)
    
    # 生成RViz启动描述
    return generate_move_group_launch(moveit_config)
