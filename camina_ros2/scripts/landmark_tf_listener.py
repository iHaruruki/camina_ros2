#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.duration import Duration
from std_msgs.msg import Float32MultiArray
from geometry_msgs.msg import TransformStamped
import tf2_ros


class LandmarkTfListenerNode(Node):
    def __init__(self):
        super().__init__('landmark_tf_listener')

        # ==== Parameters ====
        self.declare_parameter('camera_frame', 'camera_front_depth_optical_frame')
        # 監視する prefix 群（必要なものだけ残す・増やす）
        self.declare_parameter(
            'listen_prefixes',
            [
                'front_camera_pose',
                'front_camera_left_hand',
                'front_camera_right_hand',
                'front_camera_face',
                'front_camera_body',
            ]
        )
        # 出力フレーム（空なら camera_frame のまま）
        self.declare_parameter('output_frame', '')

        self.camera_frame = self.get_parameter('camera_frame').value
        self.listen_prefixes = list(self.get_parameter('listen_prefixes').value)
        self.output_frame = self.get_parameter('output_frame').value or self.camera_frame

        # ==== TF Buffer & Listener ====
        self.tf_buffer = tf2_ros.Buffer(cache_time=Duration(seconds=10.0))
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

        # ==== Publishers ====
        # x, y, z 座標を [x0, y0, z0, x1, y1, z1, ...] 形式で配信
        self.pose_pub = self.create_publisher(Float32MultiArray, '/front_camera/pose_landmarks_tf', 10)
        self.left_hand_pub = self.create_publisher(Float32MultiArray, '/front_camera/left_hand_landmarks_tf', 10)
        self.right_hand_pub = self.create_publisher(Float32MultiArray, '/front_camera/right_hand_landmarks_tf', 10)
        self.face_pub = self.create_publisher(Float32MultiArray, '/front_camera/face_landmarks_tf', 10)
        self.body_pub = self.create_publisher(Float32MultiArray, '/front_camera/body_landmarks_tf', 10)

        # どの prefix をどの publisher に流すかのマップ
        self.prefix_to_pub = {
            'front_camera_pose': self.pose_pub,
            'front_camera_left_hand': self.left_hand_pub,
            'front_camera_right_hand': self.right_hand_pub,
            'front_camera_face': self.face_pub,
            'front_camera_body': self.body_pub,
        }

        # ==== Timer ====
        # 定期的に TF を読み取って配信
        self.timer_period = 1.0 / 30.0  # 30 Hz
        self.timer = self.create_timer(self.timer_period, self.timer_callback)

        self.get_logger().info('LandmarkTfListenerNode initialized')

    def timer_callback(self):
        now = self.get_clock().now().to_msg()

        for prefix in self.listen_prefixes:
            pub = self.prefix_to_pub.get(prefix, None)
            if pub is None:
                # 対応する publisher が無ければスキップ
                continue

            coords_flat = []
            index = 0

            # 連番で存在する child frame を走査する
            while True:
                child_frame_id = f'{prefix}_{index}'

                try:
                    # 出力 frame に変換
                    tf: TransformStamped = self.tf_buffer.lookup_transform(
                        self.output_frame,
                        child_frame_id,
                        rclpy.time.Time().to_msg(),   # latest
                        timeout=Duration(seconds=0.01)
                    )
                except Exception:
                    # index=0 でも取れなかった場合は「その prefix はまだ無い」と判断
                    if index == 0:
                        # self.get_logger().debug(f'no transform for {child_frame_id}')
                        pass
                    break

                t = tf.transform.translation
                coords_flat.extend([t.x, t.y, t.z])
                index += 1

            # 何か 1 つでも取れていれば配信
            if coords_flat:
                msg = Float32MultiArray()
                msg.data = coords_flat
                pub.publish(msg)

    # もし特定 prefix + index の TF を個別に取得したい場合の helper（オプション）
    def get_landmark_tf(self, prefix: str, index: int) -> TransformStamped | None:
        child_frame_id = f'{prefix}_{index}'
        try:
            tf = self.tf_buffer.lookup_transform(
                self.output_frame,
                child_frame_id,
                rclpy.time.Time().to_msg(),
                timeout=Duration(seconds=0.05)
            )
            return tf
        except Exception as e:
            self.get_logger().warn(f'Failed to lookup {child_frame_id}: {e}')
            return None


def main(args=None):
    rclpy.init(args=args)
    node = LandmarkTfListenerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()