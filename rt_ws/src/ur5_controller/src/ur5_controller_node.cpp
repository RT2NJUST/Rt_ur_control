#include <geometry_msgs/msg/pose.hpp>
#include <moveit/move_group_interface/move_group_interface.h>
#include <rclcpp/rclcpp.hpp>

class IKMoverNode : public rclcpp::Node {
public:
  IKMoverNode() : Node("ik_moveit_node") {

    move_group_ =
        std::make_shared<moveit::planning_interface::MoveGroupInterface>(
            rclcpp::Node::make_shared("move_group_node"), PLANNING_GROUP);

    subscription_ = this->create_subscription<geometry_msgs::msg::Pose>(
        "end_effector_pose", 10,
        std::bind(&IKMoverNode::pose_callback, this, std::placeholders::_1));
  }

private:
  void pose_callback(const geometry_msgs::msg::Pose::SharedPtr msg) {

    move_group_->setPoseTarget(*msg);

    moveit::planning_interface::MoveGroupInterface::Plan my_plan;
    // bool success =
    //     (move_group_->plan(my_plan) ==
    //     moveit::core::MoveItErrorCode::SUCCESS);

    // if (success) {
    //   RCLCPP_INFO(this->get_logger(),
    //               "Planning successful. Found a valid IK solution.");

    // } else {
    //   RCLCPP_WARN(this->get_logger(),
    //               "Planning failed. Could not find a valid IK solution.");
    // }
  }
  std::string PLANNING_GROUP = "manipulator";

  std::shared_ptr<moveit::planning_interface::MoveGroupInterface> move_group_;
  rclcpp::Subscription<geometry_msgs::msg::Pose>::SharedPtr subscription_;
};

int main(int argc, char *argv[]) {
  rclcpp::init(argc, argv);

  rclcpp::executors::SingleThreadedExecutor executor;
  auto node = std::make_shared<IKMoverNode>();
  executor.add_node(node);
  executor.spin();

  rclcpp::shutdown();
  return 0;
}