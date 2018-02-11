from PyQt5.QtWidgets import (QWidget, QApplication, QMainWindow,
                             QGraphicsScene, QGraphicsRectItem,
                             QGraphicsView, QGraphicsItem, QGraphicsTextItem, QGraphicsPixmapItem,
                             QGraphicsPolygonItem)
from PyQt5.QtCore import Qt, QTimer, QObject, QPointF, QLineF, QRectF
from PyQt5.QtGui import QPixmap, QPolygonF
from math import pi, sin, cos
from Bar import Bar


class Enemy(QGraphicsPixmapItem):

    def __init__(self, points_to_follow):
        super().__init__()
        # initialize keys dictionary
        self.keys = {Qt.Key_W: False, Qt.Key_A: False,
                     Qt.Key_D: False, Qt.Key_S: False}
        self.points = points_to_follow
        self.dest = QPointF()
        self.point_index = 0
        self.team = 1

        # set graphics
        self.setPixmap(QPixmap('./res/imgs/enemy_3.png').scaled(50, 50, Qt.KeepAspectRatio))
        self.setTransformOriginPoint(25, 25)

        self.point_index = 0
        self.dest = self.points[self.point_index]
        self.rotate_to_point(self.dest)

        # connect timer to move forward
        # self.timer = QTimer()
        # self.timer.timeout.connect(self.move_forward)
        # self.timer.start(150)

        # WASD timer
        self.move_timer = QTimer()
        self.move_timer.timeout.connect(self.timer_event)
        self.move_timer.start(1000 / 60)

        # set animations
        self.current_frame = 0
        self.sprite_image = QPixmap('./res/imgs/player-move.png')

        # initialize health bar
        self.health = 100
        self.max_health = 100
        self.health_bar = Bar(self)
        self.health_bar.set_max_val(100)
        self.health_bar.set_current_val(100)

        # create a timer to change the frame
        self.sprite_timer = QTimer()
        self.sprite_timer.timeout.connect(self.nextFrame)

    def is_damageable(self):
        return True

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

    def move_forward(self):
        # if close to dest, rotate to next dest
        ln = QLineF(self.pos(), self.dest)
        if ln.length() < 5:
            if self.point_index + 1 >= len(self.points):
                self.timer.stop()
                self.timer.disconnect()
            else:
                self.point_index += 1
                self.dest = self.points[self.point_index]
                self.rotate_to_point(self.dest)

        STEP_SIZE = 5
        theta = self.rotation()     # degrees
        theta = theta * pi / 180    # radians
        dx = STEP_SIZE * cos(theta)
        dy = STEP_SIZE * sin(theta)

        # move enemy forward at current alnge
        self.setPos(self.x() + dx, self.y() + dy)

    def rotate_to_point(self, point):
        '''point: QPointF'''
        ln = QLineF(self.pos(), point)
        # that 90 is because sprite sheet is pointing north
        self.setRotation(-1 * ln.angle() + 90)

    def keyPressEvent(self, event):
        if event.key() in self.keys:
            self.keys[event.key()] = True
            self.sprite_timer.start(25)
        super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        self.keys[event.key()] = False
        if self.sprite_timer.isActive():
            self.sprite_timer.stop()
        super().keyReleaseEvent(event)

    def timer_event(self):
        # move in the direction of the rotation
        # had to change the angles because sprite sheet is pointing north
        if self.keys[Qt.Key_W]:
            theta = self.rotation() + 270     # degrees
        elif self.keys[Qt.Key_A]:
            theta = self.rotation() + 180
        elif self.keys[Qt.Key_D]:
            theta = self.rotation()
        elif self.keys[Qt.Key_S]:
            theta = self.rotation() + 90
        else:
            return

        STEP_SIZE = 5
        theta = theta * pi / 180    # radians
        dx = STEP_SIZE * cos(theta)
        dy = STEP_SIZE * sin(theta)

        # move enemy forward at current alnge
        self.setPos(self.x() + dx, self.y() + dy)
