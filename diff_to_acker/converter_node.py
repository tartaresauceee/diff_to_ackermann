import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist

import math
import numpy as np

class DiffToAckermann(Node):
    def __init__(self):
        super().__init__('diff_to_ackermann')

        # Vehicle parameters
        self.L = 0.34058 + 0.2078 # Wheel base length [m]
        self.theta_max = 0.69 # Maximum steering angle [0, pi/2]rad
        self.R_min = self.L / math.tan(self.theta_max) # Minimum turning radius

        # Subscriber to '/cmd_vel_acker' topic: Differential drive commands
        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel_diff',
            self.listener_callback,
            10
        )

        # Publisher to '/cmd_vel' topic: Ackermann commands
        self.publisher = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

    def listener_callback(self, msg):
        # Extract differential drive commands
        V_d = msg.linear.x # Forward speed
        w_d = msg.angular.z # Angular speed

        # Apply conversion
        V_scale = 0.1 # Scaling factor for the decaying gaussian
        V_a = V_d + np.copysign(1.0, V_d) * (self.R_min*np.abs(w_d)) * math.exp(-V_d**2/V_scale**2) # Forward speed
        if np.abs(V_a) < 1e-4:
            Theta_a = 0.0
        else:
            Theta_a = math.atan(self.L * w_d/V_a)

        out_msg = Twist()
        out_msg.linear.x = V_a
        out_msg.angular.z = np.clip(Theta_a, -self.theta_max, self.theta_max)

        self.publisher.publish(out_msg)

def main(args=None):
    rclpy.init(args=args)
    node = DiffToAckermann()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()