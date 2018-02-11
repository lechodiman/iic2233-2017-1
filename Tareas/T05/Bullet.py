from PyQt5.QtWidgets import (QWidget, QFrame, QApplication, QMainWindow,
                             QGraphicsScene, QGraphicsRectItem,
                             QGraphicsView, QGraphicsItem, QGraphicsTextItem, QGraphicsPixmapItem,
                             QGraphicsPolygonItem)
from PyQt5.QtCore import Qt, QTimer, QObject, QUrl, QPointF, QLineF, QRectF
from PyQt5.QtGui import QFont, QPixmap, QImage, QBrush, QPolygonF
from math import sin, cos, pi
from Sprite import Sprite


class Bullet(QGraphicsPixmapItem):
    def __init__(self, owner):
        super().__init__()
        self.max_range = owner.range
        self.distance_traveled = 0
        self.damage = owner.attack
        self.owner = owner

        # set graphics
        self.setPixmap(QPixmap('./res/imgs/tiny_bullet.png'))

        # move timer
        self.move_timer = QTimer()
        self.move_timer.timeout.connect(self.move)
        self.move_timer.start(50)

    def set_damage(self, dmg):
        self.damage = dmg

    def set_range(self, n):
        self.max_range = n

    def move(self):
        STEP_SIZE = 30
        theta = self.rotation()     # degrees
        theta = theta * pi / 180    # radians
        dx = STEP_SIZE * cos(theta)
        dy = STEP_SIZE * sin(theta)

        if self.distance_traveled > self.max_range:
            if not self.scene():
                return
            self.scene().removeItem(self)
            del self
        else:
            # move bullet
            self.setPos(self.x() + dx, self.y() + dy)
            self.distance_traveled += STEP_SIZE

            # if bullet collides with enemy, destroy both
            self.colliding_items = self.collidingItems()
            for i in self.colliding_items:
                if hasattr(i, 'team') and i.team != self.owner.team:
                    # substract health
                    if i.is_damageable():
                        i.decrease_health(self.damage)

                    # animate
                    self.scene().addItem(Sprite(self.pos()))
                    self.scene().removeItem(self)
                    del self
                    return

    def getMaxRange(self):
        return self.max_range

    def setMaxRange(self, value):
        self.max_range = value

    def getDistanceTraveled(self):
        return self.distance_traveled

    def setDistanceTraveled(self, value):
        self.distance_traveled = value
