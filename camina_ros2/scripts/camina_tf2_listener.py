import math 

from geometry_msgs.msg import Twist

import rclpy
from rclpy.node import Node


from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener

from turtlesim.srv import Spawn

class FrameListener(Node):
    
    def __init__(self):
        super().__init__('camina_tf2_frame_listener')
        
        # Declare and acquire `target_frame` parameter
        self.target_frame = self.declare_parameter(
            'target_frame', 'camera_front_link').get_parameter_value().string_value
        
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        
        # Create a client to spawn a landmark
        self.spawner = self.create_client(Spawn, 'spawn')
        self.landmark_spqwing_service_ready = False
        self.landmark_spawned = False
        
        # Create publisher
        self.publisher = self.create_publisher(Twist, 'turtle2/cmd_vel', 1)
        
        # Call on_timer function ecery second
        self.timer = self.create_timer
        
    def on_timer(self):
        from_frame_rel = self.target_frame
        to_frame_rel = 'turtle2'
        
        if self.landmark_spqwing_service_ready:
            if self.landmark_spawned:
                try:
                    t =  self.tf_buffer.lookup_transform(
                        to_frame_rel,
                        from_frame_rel,
                        rclpy.time.Time())
                except TransformException as ex:
                    self.get_logger().info(
                        f'Could not transform {to_frame_rel} to {from_frame_rel}: {ex}')
                    return
                
                msg = Twist()
                scale_rotation_rate = 1.0
                msg.angular
        