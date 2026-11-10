import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

ZAMAN_ADIMI = 0.1
ILERI_HIZ = 2.0
YARICAP = 0.5
DONUS_HIZI = ILERI_HIZ / YARICAP

class DaireCizici(Node):
    def __init__(self):
        super().__init__('dairecizici')
        self.publisher = self.create_publisher(Twist,'/turtle1/cmd_vel',10)
        self.timer = self.create_timer(ZAMAN_ADIMI,self.hareket_et)
    def hareket_et(self):
        mesaj = Twist()
        mesaj.linear.x = ILERI_HIZ
        mesaj.angular.z = DONUS_HIZI
        self.publisher.publish(mesaj)
def main():
    rclpy.init()
    node = DaireCizici()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.publisher.publish(Twist())    
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()