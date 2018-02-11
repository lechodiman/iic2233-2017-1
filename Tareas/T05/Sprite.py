from PyQt5.QtWidgets import (QWidget, QFrame, QApplication, QMainWindow,
                             QGraphicsScene, QGraphicsRectItem,
                             QGraphicsView, QGraphicsItem, QGraphicsTextItem, QGraphicsPixmapItem,
                             QGraphicsPolygonItem)
from PyQt5.QtCore import Qt, QTimer, QObject, QUrl, QPointF, QLineF, pyqtSignal, QRectF
from PyQt5.QtGui import QFont, QPixmap, QImage, QBrush, QPolygonF, QCursor
from math import pi, cos, sin


class Sprite(QGraphicsItem):
    def __init__(self, point, parent=None):
        super().__init__(parent)
        self.setPos(point)
        self.current_frame = 0
        self.sprite_image = QPixmap('./res/imgs/bullet_sprite.png')

        # create a timer to change the frame
        self.timer = QTimer()
        self.timer.timeout.connect(self.nextFrame)
        self.timer.start(25)

    def nextFrame(self):
        if not self.scene():
            return
        self.current_frame += 20
        if self.current_frame >= 300:
            # if shots are over, then remove the explosion object
            self.scene().removeItem(self)
            del self
        else:
            self.update(-10, -10, 20, 20)

    def boundingRect(self):
        return QRectF(-10, -10, 20, 20)

    def paint(self, painter, option, widget):
        # draw one of the frames of the explosion
        painter.drawPixmap(-10, -10, self.sprite_image, self.current_frame,
                           0, 20, 20)


class PlayerSprite(QGraphicsPixmapItem):
    '''Class to try and see how sprites work, it was not used it the actual game '''

    def __init__(self, parent=None):
        super().__init__(parent)
        self.keys = {Qt.Key_W: False, Qt.Key_A: False,
                     Qt.Key_D: False, Qt.Key_S: False}

        self.current_frame = 0
        self.sprite_image = QPixmap('./res/imgs/player-move.png')

        # create a timer to change the frame
        self.timer = QTimer()
        self.timer.timeout.connect(self.nextFrame)

        self.move_timer = QTimer()
        self.move_timer.timeout.connect(self.timer_event)
        self.move_timer.start(1000 / 60)

    def nextFrame(self):
        self.current_frame += 64
        if self.current_frame >= 512:
            self.current_frame = 0
        self.update(-10, -10, 64, 64)

    def boundingRect(self):
        return QRectF(-10, -10, 64, 64)

    def paint(self, painter, option, widget):
        # draw one of the frames of the player
        painter.drawPixmap(-10, -10, self.sprite_image, self.current_frame,
                           0, 64, 64)

    def keyPressEvent(self, event):
        self.keys[event.key()] = True
        print('key press')
        if event.key() == Qt.Key_W:
            self.timer.start(25)
        super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        print('key released')
        self.keys[event.key()] = False
        if event.key() == Qt.Key_W:
            self.timer.stop()
        super().keyReleaseEvent(event)

    def timer_event(self):
        # move in the direction of the rotation
        if self.keys[Qt.Key_W]:
            theta = self.rotation()     # degrees

            STEP_SIZE = 5
            theta = theta * pi / 180    # radians
            dx = STEP_SIZE * cos(theta)
            dy = STEP_SIZE * sin(theta)

            # move enemy forward at current alnge
            self.setPos(self.x() + dx, self.y() + dy)
