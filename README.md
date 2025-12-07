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
front camera
```bash
# NUC35
ros2 launch astra_camera astra_pro.launch.xml camera_name:=camera_front publish_tf:=false
```
rear camera
```bash
# NUC38
ros2 launch astra_camera astra_pro.launch.xml camera_name:=camera_rear publish_tf:=false
```

### Run `robot_state_publisher`
```bash
ros2 launch camina_ros2 camina.launch.py
```

### Run MediaPipe
Mediapipe for front camera
```bash
# NUC35
ros2 run camina_ros2 front_ramera_node
```
Mediapipe for rear camera
```bash
# NUC38
ros2 run camina_ros2 rear_ramera_node
```

## :triangular_ruler: Adjustment
### Check URDF / カメラの位置や姿勢を変更する
Change `camina_ros2/urdf/camina.urdf` file.  
`camina_ros2/urdf/camina.urdf`を変更するとカメラの位置関係を変更できる

### rviz2に`camina.urdf`を表示する
```bash
ros2 launch urdf_tutorial display.launch.py model:=$HOME/ros2_ws/src/camina_ros2/urdf/camina.urdf
```
### Check tf_tree / TFの接続関係を確認する
```bash
ros2 run tf2_tools view_frames
```
A `.pdf` file will be created in the directory where you executed it.  
実行したディレクトリに`.pdf`ファイルが作られる

### tf2_echo reports the transform between any two frames broadcast over ROS. / 特定の2つのフレーム間の変換を確認する
```bash
# ros2 run tf2_ros tf2_echo [source_frame] [target_frame]
ros2 run tf2_ros tf2_echo base_link camera_front_link
```


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

tf2
- [Introducing tf2](https://docs.ros.org/en/humble/Tutorials/Intermediate/Tf2/Introduction-To-Tf2.html)

tf2_ros / TransformBroadcaster（Python）
- [Writing a broadcaster (Python)](https://docs.ros.org/en/foxy/Tutorials/Intermediate/Tf2/Writing-A-Tf2-Broadcaster-Py.html?utm_source=chatgpt.com)
- [Writing a tf2 broadcaster (Python)[ROS1]](https://wiki.ros.org/tf2/Tutorials/Writing%20a%20tf2%20broadcaster%20%28Python%29?utm_source=chatgpt.com)

emoji
- [markdown emoji markup](https://gist.github.com/rxaviers/7360908)