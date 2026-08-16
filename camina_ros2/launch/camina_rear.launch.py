import os
import glob
import subprocess

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def _as_bool(value: str) -> bool:
    return str(value).strip().lower() in ("true", "1", "yes", "on")


def launch_setup(context, *args, **kwargs):
    share_dir = get_package_share_directory("camina_ros2")

    venv_site_pkgs = glob.glob(
        os.path.join(share_dir, ".venv", "lib", "python*", "site-packages")
    )
    existing_pythonpath = os.environ.get("PYTHONPATH", "")
    new_pythonpath = ":".join([*venv_site_pkgs, existing_pythonpath]).strip(":")

    # Base launch args
    namespace = LaunchConfiguration("namespace").perform(context)
    use_sim_time = LaunchConfiguration("use_sim_time").perform(context)

    # MediaPipe params
    min_detection_confidence = LaunchConfiguration("min_detection_confidence").perform(context)
    min_tracking_confidence = LaunchConfiguration("min_tracking_confidence").perform(context)
    model_complexity = LaunchConfiguration("model_complexity").perform(context)
    enable_segmentation = LaunchConfiguration("enable_segmentation").perform(context)

    # ROI params
    roi_enabled = LaunchConfiguration("roi_enabled").perform(context)
    roi_x = LaunchConfiguration("roi_x").perform(context)
    roi_y = LaunchConfiguration("roi_y").perform(context)
    roi_width = LaunchConfiguration("roi_width").perform(context)
    roi_height = LaunchConfiguration("roi_height").perform(context)

    # Topics / Frames
    camera_frame = LaunchConfiguration("camera_frame").perform(context)
    child_prefix = LaunchConfiguration("child_prefix").perform(context)

    # Publish settings
    publish_landmark2d = LaunchConfiguration("publish_landmark2d").perform(context)

    # TF params
    publish_pose_tf = LaunchConfiguration("publish_pose_tf").perform(context)
    tf_rate_hz = LaunchConfiguration("tf_rate_hz").perform(context)

    # Threshold params
    visibility_threshold = LaunchConfiguration("visibility_threshold").perform(context)
    presence_threshold = LaunchConfiguration("presence_threshold").perform(context)
    min_depth_m = LaunchConfiguration("min_depth_m").perform(context)
    max_depth_m = LaunchConfiguration("max_depth_m").perform(context)

    mediapipe_node_cmd = Node(
        package="camina_ros2",
        executable="holistic_pose_csv.py",
        name="holistic_pose_csv",
        namespace=namespace,
        output="screen",
        additional_env={"PYTHONPATH": new_pythonpath},
        parameters=[{
            # MediaPipe
            "min_detection_confidence": float(min_detection_confidence),
            "min_tracking_confidence": float(min_tracking_confidence),
            "model_complexity": int(model_complexity),
            "enable_segmentation": _as_bool(enable_segmentation),

            # ROI
            "roi_enabled": _as_bool(roi_enabled),
            "roi_x": int(roi_x),
            "roi_y": int(roi_y),
            "roi_width": int(roi_width),
            "roi_height": int(roi_height),

            # Topics / Frames
            "camera_frame": camera_frame,
            "child_prefix": child_prefix,

            # Landmark2D message publish settings
            "publish_landmark2d": _as_bool(publish_landmark2d),

            # TF
            "publish_pose_tf": _as_bool(publish_pose_tf),
            "tf_rate_hz": float(tf_rate_hz),

            # Thresholds
            "visibility_threshold": float(visibility_threshold),
            "presence_threshold": float(presence_threshold),
            "min_depth_m": float(min_depth_m),
            "max_depth_m": float(max_depth_m),
        }],
        remappings=[
            ("/camera/color/image_raw", "/camera_rear/color/image_raw"),
            ("/camera/color/camera_info", "/camera_rear/color/camera_info"),
            ("/camera/depth/image_raw", "/camera_rear/depth/image_raw"),
            ("/camera/depth/camera_info", "/camera_rear/depth/camera_info"),
            ("/camina/holistic/annotated_image", "/camina_rear/holistic/annotated_image"),
            ("/camina/holistic/pose/landmarks", "/camina_rear/holistic/pose/landmarks"),
            ("/camina/holistic/pose/landmarks/csv", "/camina_rear/holistic/pose/landmarks/csv"),
        ],
    )

    return [
        mediapipe_node_cmd,
    ]


def generate_launch_description():
    share_dir = get_package_share_directory("camina_ros2")
    subprocess.run(["uv", "sync", "--project", share_dir, "--no-editable"], check=True)

    return LaunchDescription([
        # Existing args
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

        # MediaPipe params
        DeclareLaunchArgument("min_detection_confidence", default_value="0.6"),
        DeclareLaunchArgument("min_tracking_confidence", default_value="0.6"),
        DeclareLaunchArgument("model_complexity", default_value="1"),
        DeclareLaunchArgument("enable_segmentation", default_value="false"),

        # ROI params
        DeclareLaunchArgument("roi_enabled", default_value="false"),
        DeclareLaunchArgument("roi_x", default_value="0"),
        DeclareLaunchArgument("roi_y", default_value="0"),
        DeclareLaunchArgument("roi_width", default_value="400"),
        DeclareLaunchArgument("roi_height", default_value="300"),

        # Topics / Frames
        DeclareLaunchArgument("camera_frame", default_value="camera_rear_depth_optical_frame"),
        DeclareLaunchArgument("child_prefix", default_value="camina_rear/mediapipe_landmark"),

        # Landmark2D publish settings
        DeclareLaunchArgument("publish_landmark2d", default_value="true"),

        # TF params
        DeclareLaunchArgument("publish_pose_tf", default_value="true"),
        DeclareLaunchArgument("tf_rate_hz", default_value="30.0"),

        # Threshold params
        DeclareLaunchArgument("visibility_threshold", default_value="0.6"),
        DeclareLaunchArgument("presence_threshold", default_value="0.0"),
        DeclareLaunchArgument("min_depth_m", default_value="0.1"),
        DeclareLaunchArgument("max_depth_m", default_value="8.0"),

        OpaqueFunction(function=launch_setup),
    ])