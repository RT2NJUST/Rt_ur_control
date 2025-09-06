#!/usr/bin/env python3
# extreme3d_servo_teleop.py
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSReliabilityPolicy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import TwistStamped
from control_msgs.msg import JointJog, GripperCommand
from std_srvs.srv import Trigger

# 常量定义（与官方C++示例保持一致）
JOY_TOPIC = "/joy"
TWIST_TOPIC = "servo_node/delta_twist_cmds"
JOINT_TOPIC = "servo_node/delta_joint_cmds"
EEF_FRAME_ID = "tool0"
BASE_FRAME_ID = "base_link"

# Logitech Extreme 3D Pro 手柄映射枚举
class Axis:
    X = 0        # 左摇杆左右
    Y = 1        # 左摇杆前后
    THROTTLE = 2 # 油门旋钮（默认值0）
    RZ = 3       # 右摇杆扭转
    HAT_X = 4    # 方向键左右
    HAT_Y = 5    # 方向键上下

class Button:
    TRIGGER = 0   # 扳机键
    THUMB = 1     # 底部左侧按钮
    THUMB2 = 2    # 底部右侧按钮
    TOP = 3       # 顶部左侧按钮
    TOP2 = 4      # 顶部右侧按钮
    BASE = 5      # 基座左侧按钮
    BASE2 = 6     # 基座右侧按钮

class Extreme3DServoTeleop(Node):
    def __init__(self):
        super().__init__("extreme3d_servo_teleop")
        
        # 参数声明（可通过ROS参数覆盖）
        self.declare_parameters(
            namespace='',
            parameters=[
                ('linear_scale', 0.3),    # 线速度缩放因子 (m/s)
                ('angular_scale', 0.15),    # 角速度缩放因子 (rad/s)
                ('joint_scale', 0.5),      # 关节速度缩放因子
                ('deadzone', 0.1),        # 摇杆死区阈值
                ('default_frame', EEF_FRAME_ID)  # 默认控制坐标系
            ]
        )
        
        # 初始化控制参数
        self.linear_scale = self.get_parameter('linear_scale').value
        self.angular_scale = self.get_parameter('angular_scale').value
        self.joint_scale = self.get_parameter('joint_scale').value
        self.deadzone = self.get_parameter('deadzone').value
        self.current_frame = self.get_parameter('default_frame').value
        
        # 配置QoS（与官方示例保持一致）
        qos_profile = QoSProfile(
            depth=10,
            reliability=QoSReliabilityPolicy.RELIABLE
        )
        
        # 创建订阅和发布者
        self.joy_sub = self.create_subscription(
            Joy, JOY_TOPIC, 
            self.joy_callback, 
            qos_profile
        )
        
        self.twist_pub = self.create_publisher(
            TwistStamped, TWIST_TOPIC, 
            qos_profile
        )
        
        self.joint_pub = self.create_publisher(
            JointJog, JOINT_TOPIC,
            qos_profile
        )
        
        self.gripper_pub = self.create_publisher(
            GripperCommand, "/gripper_command",
            qos_profile
        )
        
        # Servo控制服务客户端
        self.servo_start_client = self.create_client(
            Trigger, "/servo_node/start_servo"
        )
        while not self.servo_start_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn("等待Servo启动服务...")
        self.servo_start_client.call_async(Trigger.Request())
        
        self.get_logger().info(
            f"Logitech Extreme 3D Pro 遥操作节点已初始化\n"
            f"控制话题: {TWIST_TOPIC} (Twist) / {JOINT_TOPIC} (Joint)\n"
            f"默认控制坐标系: {self.current_frame}"
        )

    def apply_deadzone(self, value):
        """应用死区处理"""
        return 0.0 if abs(value) < self.deadzone else value

    def update_cmd_frame(self, buttons):
        """更新控制坐标系（官方示例逻辑）"""
        if buttons[Button.BASE] and self.current_frame == EEF_FRAME_ID:
            self.current_frame = BASE_FRAME_ID
            self.get_logger().info("切换至基座坐标系", throttle_duration_sec=1.0)
        elif buttons[Button.BASE2] and self.current_frame == BASE_FRAME_ID:
            self.current_frame = EEF_FRAME_ID
            self.get_logger().info("切换至末端坐标系", throttle_duration_sec=1.0)

    def joy_callback(self, msg):
        try:
            # 坐标系切换检测（使用BASE按钮）
            self.update_cmd_frame(msg.buttons)
            
            # 优先处理关节控制（使用方向键）
            if msg.axes[Axis.HAT_X] != 0 or msg.axes[Axis.HAT_Y] != 0:
                joint_cmd = JointJog()
                joint_cmd.joint_names = ["shoulder_pan_joint", "shoulder_lift_joint"]
                joint_cmd.velocities = [
                    self.apply_deadzone(msg.axes[Axis.HAT_X]) * self.joint_scale,
                    self.apply_deadzone(msg.axes[Axis.HAT_Y]) * self.joint_scale
                ]
                joint_cmd.header.stamp = self.get_clock().now().to_msg()
                joint_cmd.header.frame_id = BASE_FRAME_ID
                self.joint_pub.publish(joint_cmd)
                return
            
            # 默认处理：笛卡尔空间控制
            twist = TwistStamped()
            twist.header.stamp = self.get_clock().now().to_msg()
            twist.header.frame_id = self.current_frame
            
            # 摇杆映射（应用死区）
            twist.twist.linear.x = self.apply_deadzone(msg.axes[Axis.X]) * self.linear_scale
            twist.twist.linear.y = self.apply_deadzone(msg.axes[Axis.Y]) * self.linear_scale
            twist.twist.linear.z = self.apply_deadzone(msg.axes[Axis.THROTTLE]) * self.linear_scale
            twist.twist.angular.z = self.apply_deadzone(msg.axes[Axis.RZ]) * self.angular_scale
            
            self.twist_pub.publish(twist)
            
            # 夹爪控制（Trigger按钮）
            if msg.buttons[Button.TRIGGER] == 1:
                self.gripper_pub.publish(GripperCommand(position=0.0))
            elif msg.buttons[Button.THUMB] == 1:
                self.gripper_pub.publish(GripperCommand(position=0.8))
                
        except Exception as e:
            self.get_logger().error(f"处理手柄输入时出错: {str(e)}", throttle_duration_sec=1.0)

def main(args=None):
    rclpy.init(args=args)
    try:
        node = Extreme3DServoTeleop()
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Ctrl+C检测到,关闭节点...")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()