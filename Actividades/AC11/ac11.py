import sys
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel, QApplication, QVBoxLayout
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize
from PyQt5.QtTest import QTest
import random


class MyWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.init_game()

    def init_game(self):
        self.interrupted = False
        self.n_pairs = 0
        self.previous = ''
        self.previous_btn = None
        self.last_one = None
        self.clicks = 0
        self.intentos = 0
        self.l_1 = QLabel('Intentos: {}'.format(self.intentos))
        self.l_count = QLabel('Tiempo:  ')
        self.hide_btn = QPushButton('Ocultar')
        self.matrix = [[], [], [], [], []]
        self.button_dict = {}
        self.folder_path = 'Imgs/'
        self.imgs_id = [str(i) for i in range(1, 13)] * 2 + ['b']
        grid = QGridLayout()
        for i in range(5):
            for j in range(5):
                btn = QPushButton()
                btn.setFixedSize(50, 50)
                grid.addWidget(btn, i, j)
                icon = QIcon()
                path = 'Imgs/back.png'
                pixmap = QPixmap(path)
                icon.addPixmap(pixmap)
                btn.setIcon(icon)
                btn.setIconSize(QSize(50, 50))

                img_id_chosen = random.choice(self.imgs_id)
                self.imgs_id.remove(img_id_chosen)
                self.matrix[i].append(img_id_chosen)
                self.button_dict[btn] = (i, j)

                btn.clicked.connect(self.click_btn)

        self.hide_btn.clicked.connect(self.hide_click_btn)

        v_box = QVBoxLayout()
        v_box.addWidget(self.l_1)
        v_box.addWidget(self.l_count)
        v_box.addLayout(grid)
        v_box.addWidget(self.hide_btn)

        self.setLayout(v_box)

        self.hide_btn.setShortcut('Ctrl+A')
        for btn in self.button_dict.keys():
            btn.blocked = False

        self.show()

    def click_btn(self):
        sender = self.sender()
        if sender.blocked is True:
            return
        self.clicks += 1
        img_name = self.matrix[self.button_dict[sender][0]][self.button_dict[sender][1]]

        icon_to_show = QIcon()
        pixmap_to_show = QPixmap(self.folder_path + self.matrix[self.button_dict[sender][0]][self.button_dict[sender][1]])
        icon_to_show.addPixmap(pixmap_to_show)
        sender.setIcon(icon_to_show)

        if self.clicks % 2 == 0:
            self.intentos += 1
            self.l_1.setText('Intentos : {}'.format(self.intentos))
            if img_name == self.previous:
                self.n_pairs += 1
            else:
                self.last_one = sender

                for btn in self.button_dict.keys():
                    btn.blocked = True

                self.l_count.setText('Tiempo: 3')
                QTest.qWait(1000)

                if not self.interrupted:
                    self.l_count.setText('Tiempo: 2')
                    QTest.qWait(1000)
                if not self.interrupted:
                    self.l_count.setText('Tiempo: 1')
                    QTest.qWait(1000)

                self.l_count.setText('Tiempo: 0')
                self.interrupted = False

                for btn in self.button_dict.keys():
                    btn.blocked = False

                sender.setIcon(QIcon(QPixmap('Imgs/back.png')))
                self.previous_btn.setIcon(QIcon(QPixmap('Imgs/back.png')))

        else:
            self.previous = img_name
            self.previous_btn = sender

        if img_name == 'b':
            self.intentos += 10
            self.l_1.setText('Intentos : {}'.format(self.intentos))

        if self.n_pairs == 12:
            self.l_count.setText('Ganaste!')

    def hide_click_btn(self):
        if self.clicks == 0:
            pass
        else:
            if self.clicks % 2 == 0:
                if self.last_one is not None:
                    self.last_one.setIcon(QIcon(QPixmap('Imgs/back.png')))
                self.previous_btn.setIcon(QIcon(QPixmap('Imgs/back.png')))
                self.l_count.setText('Tiempo: 0')
                for btn in self.button_dict.keys():
                    btn.blocked = False
                self.interrupted = True
            else:
                pass

if __name__ == "__main__":

    def run():
        app = QApplication(sys.argv)
        Gui = MyWindow()
        sys.exit(app.exec_())

run()
