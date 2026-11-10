import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

# --- Ayarlar ---
KENAR_SAYISI = 1                      # şeklin kenar sayısı
ZAMAN_ADIMI = 0.1                     # hareket_et kaç saniyede bir çağrılsın
ILERI_HIZ = 1.0                       # ileri hız (birim/saniye)
ILERI_ADIM = int(80 / KENAR_SAYISI)   # toplam çevre her zaman ~8 birim
DONUS_ADIM = 10                       # 10 x 0.1 sn = 1 sn dön
DONUS_HIZ = (2 * math.pi / KENAR_SAYISI) / (DONUS_ADIM * ZAMAN_ADIMI)


class SekilCizici(Node):
    def __init__(self):
        super().__init__('sekil_cizici')
        self.publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.timer = self.create_timer(ZAMAN_ADIMI, self.hareket_et)

        # Robotun hafızası
        self.durum = 'ileri'
        self.sayac = 0
        self.kenar = 0
        self.bitti = False

        self.get_logger().info(f'{KENAR_SAYISI} kenarlı şekil çiziliyor...')

    def hareket_et(self):
        mesaj = Twist()   # tüm hızlar varsayılan olarak 0
        self.sayac += 1

        if self.durum == 'ileri':
            mesaj.linear.x = ILERI_HIZ
            if self.sayac >= ILERI_ADIM:
                self.durum = 'don'
                self.sayac = 0
                self.kenar += 1
                self.get_logger().info(f'{self.kenar}. kenar bitti')

        elif self.durum == 'don':
            mesaj.angular.z = DONUS_HIZ
            if self.sayac >= DONUS_ADIM:
                self.sayac = 0
                if self.kenar >= KENAR_SAYISI:
                    self.durum = 'bitti'
                    self.bitti = True
                    self.get_logger().info('Şekil tamamlandı!')
                else:
                    self.durum = 'ileri'

        self.publisher.publish(mesaj)


def main():
    rclpy.init()
    node = SekilCizici()
    try:
        while rclpy.ok() and not node.bitti:
            rclpy.spin_once(node)
    except KeyboardInterrupt:
        pass
    node.publisher.publish(Twist())   # çıkmadan önce son kez "dur" de
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
