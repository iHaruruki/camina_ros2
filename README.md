# camina_ros2
[![ROS 2 Distro - Humble](https://img.shields.io/badge/ros2-Humble-blue)](https://docs.ros.org/en/humble/)

## 🚀 Overview
- Whole-body pose estimation

## 📦 Feature

## 🛠️ Setup
### Camera setup
[ros2_astra_camera_setup](https://github.com/iHaruruki/ros2_astra_camera_setup.git)

### LiDAR setup
[urg_node2_setup](https://github.com/Hokuyo-aut/urg_node2.git)

### Dependent packages
```bash
sudo apt install ros-$ROS_DISTRO-urdf-tutorial ros-$ROS_DISTRO-rqt-tf-tree ros-$ROS_DISTRO-xacro ros-$ROS_DISTRO-joint-state-publisher ros-$ROS_DISTRO-joint-state-publisher-gui
```

### Clone this package
```bash
cd ~/ros2_ws/src
git clone https://github.com/iHaruruki/camina_ros2.git
```

### Build
```bash
cd ~/ros2_ws
colcon build --symlink-install --packages-select camina_ros2
source install/setup.bash
```

## 🎮 How to use
### Run Camera
```bash
# NUC35
ros2 launch astra_camera astra_pro.launch.xml camera_name:=camera_front publish_tf:=false
```
```bash
# NUC38
ros2 launch astra_camera astra_pro.launch.xml camera_name:=camera_rear publish_tf:=false
```

### Run `robot_state_publisher`
```bash
ros2 launch urdf_tutorial display.launch.py model:=$HOME/ros2_ws/src/camina_ros2/urdf/camina.urdf
```

### Run MediaPipe
```bash
# NUC35
ros2 run camina_ros2 front_ramera_node
```
```bash
# NUC38
ros2 run camina_ros2 rear_ramera_node
```

## Adjustment
### Check URDF / カメラの位置や姿勢を変更する
Change `camina_ros2/urdf/camina.urdf` file.

### rviz2に`camina.urdf`を表示する
```bash
ros2 launch urdf_tutorial display.launch.py model:=$HOME/ros2_ws/src/camina_ros2/urdf/camina.urdf
```
Check tf_tree / TFの接続関係を確認する
```bash
rqt
```
Within the `rqt` window, navigate to `Plugins -> Visualization -> TF Tree`.


## 📚 Reference
ROS2
- [ROS 2-Humble](https://docs.ros.org/en/humble/index.html)
- [ROS 2 Installation](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html)

MediaPipe Holistic
- [MediaPipe](https://chuoling.github.io/mediapipe/)
- [Holistic Landmarker](https://ai.google.dev/edge/mediapipe/solutions/vision/holistic_landmarker?utm_source=chatgpt.com)
- [MediaPipe Holistic — Simultaneous Face, Hand and Pose Prediction, on Device](https://research.google/blog/mediapipe-holistic-simultaneous-face-hand-and-pose-prediction-on-device/?utm_source=chatgpt.com)

MediaPipe Pose
- [Pose landmark detection guide](https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker?utm_source=chatgpt.com)

URDF
- [URDF](https://docs.ros.org/en/humble/Tutorials/Intermediate/URDF/URDF-Main.html)

tf2_ros / TransformBroadcaster（Python）
- [Writing a broadcaster (Python)](https://docs.ros.org/en/foxy/Tutorials/Intermediate/Tf2/Writing-A-Tf2-Broadcaster-Py.html?utm_source=chatgpt.com)
- [Writing a tf2 broadcaster (Python)[ROS1]](https://wiki.ros.org/tf2/Tutorials/Writing%20a%20tf2%20broadcaster%20%28Python%29?utm_source=chatgpt.com)
