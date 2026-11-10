import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

# --- Ayarlar ---
ZAMAN_ADIMI = 0.1      # hareket_et kaç saniyede bir çağrılsın
ILERI_HIZ = 1.0        # ileri hız (birim/saniye)
ILERI_ADIM = 20        # 20 x 0.1 sn = 2 sn düz git
DONUS_ADIM = 10        # 10 x 0.1 sn = 1 sn dön
DONUS_HIZ = (math.pi / 2) / (DONUS_ADIM * ZAMAN_ADIMI)  # tam 90 derece


class KareCizici(Node):
    def __init__(self):
        super().__init__('kare_cizici')
        self.publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.timer = self.create_timer(ZAMAN_ADIMI, self.hareket_et)

        # Robotun hafızası
        self.durum = 'ileri'
        self.sayac = 0
        self.kenar = 0

        self.get_logger().info('Kare çizici başladı!')

    def hareket_et(self):
        mesaj = Twist()   # tüm hızlar varsayılan olarak 0
        self.sayac += 1

        if self.durum == 'ileri':
            mesaj.linear.x = ILERI_HIZ
            if self.sayac >= ILERI_ADIM:
                self.durum = 'don'
                self.sayac = 0
                self.kenar += 1
                self.get_logger().info(f'{self.kenar}. kenar bitti, dönüyorum')

        elif self.durum == 'don':
            mesaj.angular.z = DONUS_HIZ
            if self.sayac >= DONUS_ADIM:
                self.sayac = 0
                if self.kenar >= 4:
                    self.durum = 'bitti'
                    self.get_logger().info('Kare tamamlandı!')
                else:
                    self.durum = 'ileri'

        # 'bitti' durumunda mesaj boş kalır, yani robot durur

        self.publisher.publish(mesaj)


def main():
    rclpy.init()
    node = KareCizici()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
		
