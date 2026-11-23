import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import mediapipe as mp

# Hand tracking
mp_hands = mp.solutions.hands
from aisd_msgs.msg import Hand


class Hands(Node):

    def __init__(self):

        # Node initialization
        super().__init__('hands')

        # Subscribe to Image, which listens for images from the camera
        self.subscription = self.create_subscription(
            Image,
            'video_frames',
            self.listener_callback,
            10)
        self.subscription

        # Convert ROS2 images to OpenCV format
        self.br = CvBridge()

        # Sends hand data
        self.hand_publisher = self.create_publisher(Hand, 'cmd_hand', 10)

    def listener_callback(self, msg):
        # Convert incoming images
        image = self.br.imgmsg_to_cv2(msg)

        # Initialization
        PINKY_FINGER_TIP = 20
        INDEX_FINGER_TIP = 8

        # Hand detection
        with mp_hands.Hands(
                model_complexity=0,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5) as myhands:
            image.flags.writeable = False

            # Convert image to the RGB values
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Detect hands
            results = myhands.process(image)

            # Check if a hand is found
            if results.multi_hand_landmarks:
                # Initialization of new Hand message
                msg = Hand()

                # Saving the x-axis position of the pinky finger fingertip
                msg.xpinky = results.multi_hand_landmarks[0].landmark[PINKY_FINGER_TIP].x

                # Saving the x-axis position of the index finger fingertip
                msg.xindex = results.multi_hand_landmarks[0].landmark[INDEX_FINGER_TIP].x

                # Send the data if subscriber is currenlty running
                if self.hand_publisher.get_subscription_count() > 0:
                    self.hand_publisher.publish(msg)
                else:
                    self.get_logger().info('waiting for subcriber')


def main(args=None):
    # Start communication in ROS 2
    rclpy.init(args=args)

    # Node object
    hands = Hands()

    # Node runs until interruption
    rclpy.spin(hands)

    # Destroy node and shut down
    hands.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
