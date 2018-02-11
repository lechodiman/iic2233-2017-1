from PyQt5.QtWidgets import (
    QGraphicsRectItem,
    QGraphicsItem, QGraphicsTextItem, QGraphicsPixmapItem,
    QGraphicsPolygonItem)
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap

from DynamicGameObject import DynamicGameObject
from Bar import Bar
from Nexus import Nexus


class Minion(DynamicGameObject):

    def __init__(self):
        super().__init__()
        # set graphics
        self.setPixmap(QPixmap('./res/imgs/knight.png'))
        self.setTransformOriginPoint(16, 16)

        # initialize health bar
        h = Bar(self)
        h.set_max_val(45)
        h.set_current_val(45)
        self.set_health(h)

        # set specs
        self.set_speed(3)
        self.set_attack(2)
        self.set_range(25)

        # set destination
        self.destination_timer = QTimer()
        self.destination_timer.timeout.connect(self.set_dest_to_closest)
        self.destination_timer.start(1000 / 30)

        # connect timer to move forward
        self.move_timer = QTimer()
        self.move_timer.timeout.connect(self.move_forward)
        self.move_timer.start(1000 / 30)

        # timer to damage
        self.damage_timer = QTimer()
        self.damage_timer.timeout.connect(self.damage_if_colliding)
        self.damage_timer.start(1000)

    def set_dest_to_nexus(self):
        if not self.collidesWithItem([i for i in self.scene().items() if isinstance(i, Nexus)].pop()):
            nexus_pos = [i.pos() for i in self.scene().items() if isinstance(i, Nexus)].pop()
            self.set_destination(nexus_pos)

    def damage_if_colliding(self):
        # damage if colliding with enemy
        self.has_target = False
        colliding_items = self.attack_area.collidingItems()
        for i in colliding_items:
            if hasattr(i, 'team') and i.team != self.team:
                i.decrease_health(self.attack)
                self.has_target = True
