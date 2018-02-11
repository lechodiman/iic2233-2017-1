from PyQt5.QtWidgets import (QWidget, QFrame, QApplication, QMainWindow,
                             QGraphicsScene, QGraphicsRectItem,
                             QGraphicsView, QGraphicsItem, QGraphicsTextItem, QGraphicsPixmapItem,
                             QGraphicsPolygonItem)
import sys
from PyQt5.QtCore import Qt, QTimer, QObject, QUrl, QPointF, QLineF
from PyQt5.QtGui import QFont, QPixmap, QImage, QBrush, QPolygonF, QPen

# sound
from Bullet import Bullet
from StaticGameObject import StaticGameObject
from Bar import Bar


class Tower(StaticGameObject):
    def __init__(self):
        super().__init__()
        # initialize attack range (area)
        self.attack_area = QGraphicsPolygonItem()
        self.attack_dest = QPointF(0, 0)
        self.has_target = False

        # set the graphics
        self.setPixmap(QPixmap('./res/imgs/lol_tower.png').
                       scaled(80, 80, Qt.KeepAspectRatio))

        # initializes health
        h = Bar(self)
        h.set_max_val(250)
        h.set_current_val(250)
        self.set_health(h)
        self.attack = 30

        # create points vector
        points = [QPointF(1, 0), QPointF(2, 0), QPointF(3, 1),
                  QPointF(3, 2), QPointF(2, 3), QPointF(1, 3),
                  QPointF(0, 2), QPointF(0, 1)]

        # scale points
        SCALE_FACTOR = 100
        points = [p * SCALE_FACTOR for p in points]
        self.range = SCALE_FACTOR

        # create polygon
        self.polygon = QPolygonF(points)

        # create QGraphicsPolygonItem
        self.attack_area = QGraphicsPolygonItem(self.polygon, self)
        self.attack_area.setPen(QPen(Qt.DotLine))

        # move the polygon
        poly_center = QPointF(1.5 * SCALE_FACTOR, 1.5 * SCALE_FACTOR)
        poly_center = self.mapToScene(poly_center)
        tower_center = QPointF(self.x() + 40, self.y() + 40)
        ln = QLineF(poly_center, tower_center)
        self.attack_area.setPos(self.x() + ln.dx(), self.y() + ln.dy())

        # connect a timer to acquire target
        self.damage_timer = QTimer()
        self.damage_timer.timeout.connect(self.acquire_target)
        self.damage_timer.start(1000)

        # allow responding to hover events
        self.setAcceptHoverEvents(True)

    def fire(self):
        if not self.scene():
            return
        bullet = Bullet(self)
        bullet.setPos(self.x() + 40, self.y() + 40)

        # set the angle to be paralel to the line that connects the
        # tower and target
        ln = QLineF(QPointF(self.x() + 40, self.y() + 40), self.attack_dest)
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

    def distance_to(self, item):
        '''item: QGraphicsItem '''
        ln = QLineF(self.pos(), item.pos())
        return ln.length()

    def hoverEnterEvent(self, event):
        '''event: QGraphicsSceneHoverEvent '''
        # change pixmap
        if self.team == 2:
            self.setPixmap(QPixmap('./res/imgs/lol_tower_red.png').
                           scaled(80, 80, Qt.KeepAspectRatio))

    def hoverLeaveEvent(self, event):
        '''event: QGraphicsSceneHoverEvent '''
        # change back pixmap
        if self.team == 2:
            self.setPixmap(QPixmap('./res/imgs/lol_tower.png').
                           scaled(80, 80, Qt.KeepAspectRatio))
