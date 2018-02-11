from PyQt5.QtWidgets import (QWidget, QFrame, QApplication, QMainWindow,
                             QGraphicsScene, QGraphicsRectItem,
                             QGraphicsView, QGraphicsItem, QGraphicsTextItem, QGraphicsPixmapItem,
                             QGraphicsPolygonItem)
from PyQt5.QtCore import Qt, QTimer, QObject, QUrl, QPointF, QLineF, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap, QImage, QBrush, QPolygonF, QCursor, QPen

from StaticGameObject import StaticGameObject
from Bullet import Bullet


class DynamicGameObject(StaticGameObject):
    '''Class to modelate objects that can move and attack (minions, Ia's champion) '''

    def __init__(self):
        super().__init__()
        # set speed
        self.speed = 0
        self.attack = 1

        # set pos / destination
        self.x_prev = 0
        self.y_prev = 0
        self.setPos(0, 0)
        self.destination = QPointF(0, 0)

        # initialize attack range (area)
        self.attack_area = QGraphicsPolygonItem()
        self.attack_dest = QPointF(0, 0)
        self.has_target = False

    def set_range(self, SCALE_FACTOR):
        '''It gives the object a QGraphicsPolygonItem to attack at a certain range '''
        # create points vector
        self.range = SCALE_FACTOR

        points = [QPointF(1, 0), QPointF(2, 0), QPointF(3, 1),
                  QPointF(3, 2), QPointF(2, 3), QPointF(1, 3),
                  QPointF(0, 2), QPointF(0, 1)]

        # scale points
        points = [p * SCALE_FACTOR for p in points]

        # create polygon
        self.polygon = QPolygonF(points)

        # create QGraphicsPolygonItem
        self.attack_area = QGraphicsPolygonItem(self.polygon, self)
        self.attack_area.setPen(QPen(Qt.DotLine))

        # move the polygon
        poly_center = QPointF(1.5 * SCALE_FACTOR, 1.5 * SCALE_FACTOR)
        poly_center = self.mapToScene(poly_center)
        minion_center = QPointF(self.x() + self.pixmap().width() / 2, self.y() + self.pixmap().height() / 2)
        ln = QLineF(poly_center, minion_center)
        self.attack_area.setPos(self.x() + ln.dx(), self.y() + ln.dy())

    def fire(self):
        if not self.scene():
            return

        bullet = Bullet(self)
        bullet.setPos(self.x() + self.pixmap().width() / 2, self.y() + self.pixmap().height() / 2)

        # set the angle to be paralel to the line that connects the
        # tower and target
        ln = QLineF(QPointF(self.x() + self.pixmap().width() / 2, self.y() + self.pixmap().height() / 2), self.attack_dest)
        angle = -1 * ln.angle()  # -1 to make it clock wise

        bullet.setRotation(angle)

        self.scene().addItem(bullet)

    def acquire_target(self):
        # get a list of all items colliding with attack area
        colliding_items = self.attack_area.collidingItems()

        self.has_target = False
        closest_dist = 300
        closest_point = QPointF(0, 0)
        for i in colliding_items:
            if hasattr(i, 'team') and i.team != self.team:
                this_distance = self.distance_to(i)
                if this_distance < closest_dist:
                    closest_dist = this_distance
                    closest_point = i.pos()
                    self.has_target = True

        self.attack_dest = closest_point
        if self.has_target:
            self.fire()

    def set_attack(self, value):
        self.attack = value

    def set_destination(self, point):
        '''QPoinF : point '''
        self.destination = point

    def set_speed(self, s):
        self.speed = s

    @property
    def should_be_moving(self):
        ln = QLineF(self.pos(), self.destination)
        CLOSE_DIST = 30

        if ln.length() > CLOSE_DIST:
            return True
        else:
            return False

    def move_forward(self):
        # move object
        if self.should_be_moving:
            ln = QLineF(self.pos(), self.destination)
            ln.setLength(self.speed)

            self.rotate_to_point(self.destination)

            # avoid collision
            colliding_items = self.collidingItems()
            for i in colliding_items:
                if isinstance(i, StaticGameObject):
                    collision_line = QLineF(self.pos(), i.pos())
                    collision_line.setLength(30)
                    self.setPos(self.x() - collision_line.dx(), self.y() - collision_line.dy())

            # move object forward at current angle
            self.setPos(self.x() + ln.dx(), self.y() + ln.dy())

        self.x_prev = self.pos().x()
        self.y_prev = self.pos().y()

    def distance_to(self, item):
        '''item: QGraphicsItem '''
        ln = QLineF(self.pos(), item.pos())
        return ln.length()

    def set_dest_to_closest(self):
        '''Sets destination to closest enemy '''
        if not self.scene():
            return
        scene_items = self.scene().items()

        closest_point = QPointF(0, 0)
        closest_dist = 1000
        for i in scene_items:
            if hasattr(i, 'team') and i.team != self.team:
                this_distance = self.distance_to(i)
                if this_distance < closest_dist:
                    closest_dist = this_distance
                    closest_point = i.pos()

        self.set_destination(closest_point)

    def rotate_to_point(self, point):
        '''point: QPointF'''
        ln = QLineF(self.pos(), point)
        # that 90 is because sprite sheet is pointing north
        self.setRotation(-1 * ln.angle() + 90)
