import os
import sys

import requests
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel,QPushButton


SCREEN_SIZE = [600, 650]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.server_address = 'https://static-maps.yandex.ru/v1?'
        self.api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
        self.theme = 'light'
        self.spn = 0.5
        self.x = 131.970229
        self.y = 43.135905
        self.initUI()
        self.getImage()
    def getImage(self):
        # Готовим запрос.

        params = {
            "apikey": self.api_key,
            'll': f'{self.x},{self.y}',
            'spn': f'{self.spn},{self.spn}',
            'theme': self.theme
        }

        response = requests.get(self.server_address, params=params)

        if not response:
            print("Ошибка выполнения запроса:")
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)

        self.update()

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        self.image = QLabel(self)

        self.up = QPushButton('↑', self)
        self.up.resize(40, 40)
        self.up.move(20, 450)

        self.right = QPushButton('→', self)
        self.right.resize(40, 40)
        self.right.move(40, 490)

        self.left = QPushButton('←', self)
        self.left.resize(40, 40)
        self.left.move(0, 490)

        self.down = QPushButton('↓', self)
        self.down.resize(40, 40)
        self.down.move(20, 530)

        self.buttom_theme = QPushButton('сменить тему', self)
        self.buttom_theme.resize(100, 40)
        self.buttom_theme.move(500, 450)

        self.up.clicked.connect(self.click_up)
        self.down.clicked.connect(self.click_down)
        self.right.clicked.connect(self.click_right)
        self.left.clicked.connect(self.click_left)
        self.buttom_theme.clicked.connect(self.change_theme)


    def click_up(self):
        self.y += 0.2
        self.getImage()

    def click_down(self):
        self.y -= 0.2
        self.getImage()

    def click_right(self):
        self.x += 0.2
        self.getImage()

    def click_left(self):
        self.x -= 0.2
        self.getImage()

    def change_theme(self):
        if self.theme == 'light':
            self.theme = 'dark'
            self.buttom_theme = QPushButton('🌑', self)
        else:
            self.theme = 'light'
            self.buttom_theme = QPushButton('☀', self)

        self.getImage()

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())

