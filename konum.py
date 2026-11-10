import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose


class KonumOkuyucu(Node):
    def __init__(self):
        super().__init__('konum_okuyucu')
        self.subscription = self.create_subscription(
            Pose, '/turtle1/pose', self.konum_geldi, 10)

    def konum_geldi(self, konum):
        self.get_logger().info(
            f'x={konum.x:.2f}  y={konum.y:.2f}  yon={konum.theta:.2f}')


def main():
    rclpy.init()
    node = KonumOkuyucu()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
