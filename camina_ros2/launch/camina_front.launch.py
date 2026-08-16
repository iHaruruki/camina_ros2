import os
import glob
import subprocess

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    share_dir = get_package_share_directory("camina_ros2")
    subprocess.run(["uv", "sync", "--project", share_dir, "--no-editable"], check=True)
    venv_site_pkgs = glob.glob(
        os.path.join(share_dir, ".venv", "lib", "python*", "site-packages")
    )
    existing_pythonpath = os.environ.get("PYTHONPATH", "")
    new_pythonpath = ":".join([*venv_site_pkgs, existing_pythonpath]).strip(":")

    urdf_file_path_cmd = DeclareLaunchArgument(
        "urdf_file_path",
        default_value="camina_front",
        description="urdf file path",
    )

    rviz_config_path_cmd = DeclareLaunchArgument(
        "rviz_config_path",
        default_value="camina_front",
        description="rviz config file path",
    )

    namespace_cmd = DeclareLaunchArgument(
        "namespace",
        default_value="camina_front",
        description="Namespace for the nodes",
    )

    use_sim_time_cmd = DeclareLaunchArgument(
        "use_sim_time",
        default_value="false",
        description="Use simulation (Gazebo) clock if true",
    )

    namespace = LaunchConfiguration("namespace")
    use_sim_time = LaunchConfiguration("use_sim_time")
    urdf_path = os.path.join(LaunchConfiguration("urdf_file_path"))
    with open(urdf_path, "r") as f:
        robot_desc = f.read()
    rviz_config_dir = os.path.join(LaunchConfiguration("rviz_config_path"))

    mediapipe_node_cmd = Node(
        package="camina_ros2",
        executable="holistic_pose_csv.py",
        name="holistic_pose_csv",
        namespace=namespace,
        output="screen",
        additional_env={"PYTHONPATH": new_pythonpath},
    )

    robot_state_publisher_cmd = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[{
            "use_sim_time": use_sim_time,
            "robot_description": robot_desc,
        }],
    )

    rviz_cmd = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        arguments=["-d", rviz_config_dir],
        output="screen",
    )

    return LaunchDescription([
        urdf_file_path_cmd,
        rviz_config_path_cmd,
        namespace_cmd,
        use_sim_time_cmd,
        mediapipe_node_cmd,
        robot_state_publisher_cmd,
        rviz_cmd,
    ])