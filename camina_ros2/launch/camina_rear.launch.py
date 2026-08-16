import os
import glob
import subprocess

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def launch_setup(context, *args, **kwargs):
    share_dir = get_package_share_directory("camina_ros2")

    venv_site_pkgs = glob.glob(
        os.path.join(share_dir, ".venv", "lib", "python*", "site-packages")
    )
    existing_pythonpath = os.environ.get("PYTHONPATH", "")
    new_pythonpath = ":".join([*venv_site_pkgs, existing_pythonpath]).strip(":")

    namespace = LaunchConfiguration("namespace").perform(context)
    use_sim_time = LaunchConfiguration("use_sim_time").perform(context)

    mediapipe_node_cmd = Node(
        package="camina_ros2",
        executable="holistic_pose_csv.py",
        name="holistic_pose_csv",
        namespace=namespace,
        output="screen",
        additional_env={"PYTHONPATH": new_pythonpath},
    )

    return [
        mediapipe_node_cmd,
    ]


def generate_launch_description():
    share_dir = get_package_share_directory("camina_ros2")
    subprocess.run(["uv", "sync", "--project", share_dir, "--no-editable"], check=True)

    return LaunchDescription([
        DeclareLaunchArgument(
            "namespace",
            default_value="camina_rear",
            description="Namespace for the nodes",
        ),
        DeclareLaunchArgument(
            "use_sim_time",
            default_value="false",
            description="Use simulation (Gazebo) clock if true",
        ),
        OpaqueFunction(function=launch_setup),
    ])