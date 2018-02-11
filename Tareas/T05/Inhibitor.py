from PyQt5.QtWidgets import (QWidget, QFrame, QApplication, QMainWindow,
                             QGraphicsScene, QGraphicsRectItem,
                             QGraphicsView, QGraphicsItem, QGraphicsTextItem, QGraphicsPixmapItem,
                             QGraphicsPolygonItem)
import sys
from PyQt5.QtCore import Qt, QTimer, QObject, QUrl, QPointF, QLineF, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap, QImage, QBrush, QPolygonF, QPen

from StaticGameObject import StaticGameObject
from Bar import Bar


class InhibitorSignal(QObject):
    '''This signal will be connected to make nexus damageable
    and spawn stronger minions function'''
    died = pyqtSignal()


class Inhibitor(StaticGameObject):

    def __init__(self):
        super().__init__()

        # set the graphics
        self.setPixmap(QPixmap('./res/imgs/lol_inhibitor_2.png').
                       scaled(50, 50, Qt.KeepAspectRatio))

        # initializes health
        h = Bar(self)
        h.set_max_val(600)
        h.set_current_val(600)
        self.set_health(h)

        # initializes signal (when it dies)
        self.s = InhibitorSignal()

        # allow responding to hover events
        self.setAcceptHoverEvents(True)

    def decrease_health(self, value):
        '''Overriding decrease health to emit a signal if it dies '''
        self.health.decrement(value)

        if self.health.get_current_val() <= 0:
            # emit the signal before erase from existance
            self.s.died.emit()

            # hasta la vista, baby
            self.scene().removeItem(self)
            del self

    def hoverEnterEvent(self, event):
        '''event: QGraphicsSceneHoverEvent '''
        # change pixmap
        if self.team == 2:
            self.setPixmap(QPixmap('./res/imgs/lol_inhibitor_2_red.png').
                           scaled(50, 50, Qt.KeepAspectRatio))

    def hoverLeaveEvent(self, event):
        '''event: QGraphicsSceneHoverEvent '''
        # change back pixmap
        if self.team == 2:
            self.setPixmap(QPixmap('./res/imgs/lol_inhibitor_2.png').
                           scaled(50, 50, Qt.KeepAspectRatio))
