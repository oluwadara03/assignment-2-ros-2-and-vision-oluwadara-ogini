import rclpy
from rclpy.node import Node

from aisd_msgs.msg import Hand
from geometry_msgs.msg import Twist


class Move(Node):

    # Initialize the ROS 2 node with the name 'move'
    def __init__(self):
        super().__init__('move')

        # Hand tracking
        self.subscription = self.create_subscription(
            Hand,
            'cmd_hand',
            self.listener_callback,
            10)
        self.subscription
        self.vel_publisher = self.create_publisher(Twist, 'cmd_vel', 10)

    def listener_callback(self, msg):
        # Default initialization
        angle = 0.0
        linear = 0.0

        # Establish turning direction by observing the horizontal index finger position
        if msg.xindex > 0.55:
            self.get_logger().info('right')
            angle = -0.1
        elif msg.xindex < 0.45:
            self.get_logger().info('left')
            angle = 0.1
        else:
            angle = 0.0

        # Establish forward movement by comparing the hand index and pinky positions
        if msg.xindex > msg.xpinky:
            self.get_logger().info('come')
            linear = 0.5
        else:
            self.get_logger().info('stay')
            linear = 0.0
        twist = Twist()
        twist.linear.x = linear
        twist.angular.z = angle
        if self.vel_publisher.get_subscription_count() > 0:
            self.vel_publisher.publish(twist)
        else:
            self.get_logger().info('waiting for subcriber')


def main(args=None):
    rclpy.init(args=args)
    move = Move()
    rclpy.spin(move)

    # Clean up and shut down ROS 2 on exit
    move.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
