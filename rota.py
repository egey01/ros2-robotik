import math
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

ROTA = [(2, 8), (9, 9), (9, 2), (5.5, 5.5)]
K_HIZ = 3.0
MAKS_HIZ = 2.0
K_DONUS = 4.0
TOLERANS = 0.1


class HedefeGidici(Node):
    def __init__(self):
        super().__init__('hedefe_gidici')
        self.subscription = self.create_subscription(
            Pose, '/turtle1/pose', self.konum_geldi, 10)
        self.publisher = self.create_publisher(Twist,'/turtle1/cmd_vel',10)
        self.hedef_no = 0
        if self.hedef_no >= len(ROTA):
            mesaj = Twist()
            return
        
    def konum_geldi(self, konum):
        if self.hedef_no >= len(ROTA):
            self.publisher.publish(Twist())
            return

        hedef_x, hedef_Y = ROTA[self.hedef_no]
        dx = hedef_x - konum.x
        dy = hedef_Y - konum.y
        mesafe = math.hypot(dx, dy)
        hedef_aci = math.atan2(dy, dx)
        aci_farki = hedef_aci - konum.theta
        aci_farki = math.atan2(math.sin(aci_farki), math.cos(aci_farki))
        
        mesaj = Twist()
        if mesafe > TOLERANS:
            mesaj.linear.x = min(K_HIZ * mesafe, MAKS_HIZ) 
            mesaj.angular.z = K_DONUS * aci_farki
        else:
            self.get_logger().info(
                f'{self.hedef_no + 1}. hedefe varıldı'
            )
            self.hedef_no += 1
        if self.hedef_no >= len(ROTA):
            mesaj = Twist()
            return
        self.publisher.publish(mesaj)

def main():
    rclpy.init()
    node = HedefeGidici()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.publisher.publish(Twist())
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
