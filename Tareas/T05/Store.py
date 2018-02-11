import sys
from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QApplication, QSlider, QCheckBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize


class Store(QWidget):
    '''Gui for the store '''

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.title_label = QLabel('Store')
        v_box = QVBoxLayout()

        h_box_title = QHBoxLayout()
        h_box_title.addStretch()
        h_box_title.addWidget(self.title_label)
        h_box_title.addStretch()

        v_box.addLayout(h_box_title)
        for i in range(0, 6):
            horizontal = QHBoxLayout()
            btn = QPushButton(QIcon('./res/imgs/Store/{}'.format(i)), 'Buy')
            btn.setIconSize(QSize(50, 50))
            horizontal.addWidget(btn)
            vertical = QVBoxLayout()
            cost = QLabel('Cost : 0')
            upgrade = QLabel('Upgrade : +0')
            vertical.addWidget(cost)
            vertical.addWidget(upgrade)
            horizontal.addLayout(vertical)

            v_box.addLayout(horizontal)

        self.setLayout(v_box)


if __name__ == "__main__":

    def run():
        app = QApplication(sys.argv)
        Gui = Store()
        Gui.show()
        sys.exit(app.exec_())

    run()
