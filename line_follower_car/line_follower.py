import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge
import cv2
import numpy as np

class LineFollower(Node):
    def __init__(self):
        super().__init__("line_follower")
        self.publisher = self.create_publisher(Twist, "/model/car/cmd_vel", 10)
        self.subscription = self.create_subscription(
            Image, "/camera/image_raw", self.image_callback, 10)
        self.bridge = CvBridge()
        self.get_logger().info("Line Follower démarré !")

    def image_callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        h, w = frame.shape[:2]

        # Prendre seulement la partie basse
        roi = frame[int(h*0.5):h, :]

        # Détection blanc avec seuil large
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

        M = cv2.moments(mask)
        twist = Twist()

        if M["m00"] > 100:
            cx = int(M["m10"] / M["m00"])
            error = cx - w // 2
            self.get_logger().info(f"Ligne trouvée! cx={cx} error={error}")
            twist.linear.x = 0.3
            twist.angular.z = -float(error) / 150.0
        else:
            self.get_logger().info("Ligne perdue!")
            twist.linear.x = 0.0
            twist.angular.z = 0.3

        self.publisher.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = LineFollower()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
