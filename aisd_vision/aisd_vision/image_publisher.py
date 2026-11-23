import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge
import cv2


class ImagePublisher(Node):

    def __init__(self):
        # Initialization of the ROS 2 node
        super().__init__('image_publisher')

        # Creating publisher to send camera frames
        self.publisher_ = self.create_publisher(Image, 'video_frames', 10)

        # Capture and publish camera frames every 0.1 seconds
        timer_period = 0.1
        self.timer = self.create_timer(timer_period, self.timer_callback)

        # Default webcam being used for image conversion
        self.cap = cv2.VideoCapture(1)
        self.br = CvBridge()

    def timer_callback(self):
        # Capture frames from the webcam
        ret, frame = self.cap.read()
        if ret == True:
            self.publisher_.publish(self.br.cv2_to_imgmsg(frame))


def main(args=None):
    # Initialization
    rclpy.init(args=args)
    
    # Create the node
    image_publisher = ImagePublisher()
    rclpy.spin(image_publisher)

    # Clean up and shut down ROS 2 on user exit
    image_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
