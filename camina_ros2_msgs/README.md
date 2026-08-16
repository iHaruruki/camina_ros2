## 🚀 Overview
`mediapipe_ros2_msgs`is a small ROS 2 interface package that defines message types for streaming 2D landmark results produced by MediaPipe.  
`mediapipe_ros2_msgs` は、MediaPipe によって生成された 2D ランドマーク結果をストリーミングするためのメッセージ タイプを定義する小さな ROS 2 インターフェース パッケージです。

## 📦 Defines message type
```yaml
std_msgs/Header header   # time and frame_id / 同期元(color)の時刻/座標系
string name              # landmark name / ランドマーク名（nose, left_eye_inner, ...）
uint16 index             # numeric landmark index / ランドマークid
float32 x                # pixel coordinates in the full image / 画像ピクセルx（フル画像座標）
float32 y                # pixel coordinates in the full image / 画像ピクセルy（フル画像座標）
```

## 📚 References
- [Creating custom msg and srv files](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Custom-ROS2-Interfaces.html)
