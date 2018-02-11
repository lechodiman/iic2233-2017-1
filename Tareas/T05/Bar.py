from PyQt5.QtWidgets import (
    QGraphicsRectItem,
    QGraphicsTextItem
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class Bar(QGraphicsRectItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.max_val = 1
        self.current_val = 1

        self.WIDTH = parent.pixmap().width() if parent else 60
        self.setRect(parent.pos().x(), parent.pos().y(), self.WIDTH, 8)
        self.setBrush(Qt.red)

        self.text = QGraphicsTextItem(self)
        self.text.setDefaultTextColor(Qt.white)
        font = QFont('comic sans', 7)
        self.text.setFont(font)
        self.text.setPos(self.x(), self.y() - 7)

    def update_bar(self):
        # updates the bar graphics to the current amount of fullnes
        fill_fraction = float(self.current_val) / self.max_val
        self.text.setPlainText('{} / {}'.format(self.current_val, self.max_val))
        self.setRect(self.rect().x(), self.rect().y(), fill_fraction * self.WIDTH, 8)

    def get_current_val(self):
        return self.current_val

    def set_current_val(self, value):
        self.current_val = value

    def set_max_val(self, value):
        self.max_val = value

    def increment(self, amount):
        # increase the amount the bar is filled and updates it
        self.current_val += amount
        self.update_bar()

    def decrement(self, amount):
        # decreases and updates
        self.current_val -= amount
        self.update_bar()
