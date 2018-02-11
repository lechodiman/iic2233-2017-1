from PyQt5.QtWidgets import (QWidget, QFrame, QApplication, QMainWindow,
                             QGraphicsScene, QGraphicsRectItem,
                             QGraphicsView, QGraphicsItem, QGraphicsTextItem, QGraphicsPixmapItem,
                             QGraphicsPolygonItem)
from PyQt5.QtCore import Qt, QTimer, QObject, QUrl, QPointF, QLineF, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap, QImage, QBrush, QPolygonF, QCursor, QPen

from DynamicGameObject import DynamicGameObject
from Bar import Bar


class BigMinion(DynamicGameObject):

    def __init__(self, powered_up=False):
        super().__init__()
        # set graphics
        if not powered_up:
            self.setPixmap(QPixmap('./res/imgs/wizard.png').scaled(40, 40, Qt.KeepAspectRatio))
            self.setTransformOriginPoint(20, 20)
            h = Bar(self)
            h.set_max_val(60)
            h.set_current_val(60)
            self.set_health(h)
            self.set_attack(4)

        else:
            self.setPixmap(QPixmap('./res/imgs/wizard.png').scaled(60, 60, Qt.KeepAspectRatio))
            self.setTransformOriginPoint(30, 30)
            h = Bar(self)
            h.set_max_val(120)
            h.set_current_val(120)
            self.set_health(h)
            self.set_attack(10)

        # set specs
        self.set_speed(2)

        # set attack area
        self.set_range(100)

        # connect a timer to acquire target
        self.damage_timer = QTimer()
        self.damage_timer.timeout.connect(self.acquire_target)
        self.damage_timer.start(1000)

        # timer to move forward, but if has target, then it does not move
        self.move_timer = QTimer()
        self.move_timer.timeout.connect(self.move_forward)
        self.move_timer.start(1000 / 30)

        # set destination
        self.destination_timer = QTimer()
        self.destination_timer.timeout.connect(self.set_dest_to_closest)
        self.destination_timer.start(1000 / 30)

    def move_forward(self):
        '''Overwiting this method to stop moving if has target '''
        if self.has_target:
            return
        else:
            super().move_forward()
