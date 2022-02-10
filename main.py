import os
import sys
import math
import requests
import geocoder
import distance
import business
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PIL import Image
from io import BytesIO

SCREEN_SIZE = [600, 450]
a = 1
LAT_STEP = 0.002
LON_STEP = 0.002
coord_to_geo = 0.0000428

my_object = (37.530887, 55.703118)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.map_file = "map.png"
        self.lon = my_object[0]
        self.lat = my_object[1]
        self.z = 14
        self.lat_step = LAT_STEP
        self.lon_step = LON_STEP
        self.initUI()
        self.view_image()

    def getImage(self):
        params = {
            'll': f'{self.lon},{self.lat}',
            'z': self.z,
            'l': 'map'
        }
        map_request = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_request, params=params)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def view_image(self):
        self.getImage()
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Большая задача по Maps')

        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(SCREEN_SIZE[0], SCREEN_SIZE[1])

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp and self.z < 20:
            self.z += 1
            self.lat_step /= 2
            self.lon_step /= 2
            self.view_image()
        elif event.key() == Qt.Key_PageDown and self.z > 0:
            self.z -= 1
            self.lat_step *= 2
            self.lon_step *= 2
            self.view_image()


    def closeEvent(self, event):
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
