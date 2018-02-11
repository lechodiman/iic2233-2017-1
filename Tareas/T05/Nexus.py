from PyQt5.QtWidgets import (QWidget, QFrame, QApplication, QMainWindow,
                             QGraphicsScene, QGraphicsRectItem,
                             QGraphicsView, QGraphicsItem, QGraphicsTextItem, QGraphicsPixmapItem,
                             QGraphicsPolygonItem)
from PyQt5.QtCore import Qt, QTimer, QObject, QUrl, QPointF, QLineF, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap, QImage, QBrush, QPolygonF, QPen

from StaticGameObject import StaticGameObject
from Bar import Bar


class NexusSignal(QObject):
    '''This signal will be connected to game over function '''
    died = pyqtSignal()


class Nexus(StaticGameObject):

    def __init__(self,):
        super().__init__()
        # set the graphics
        self.setPixmap(QPixmap('./res/imgs/lol_nexus_1.png').
                       scaled(80, 80, Qt.KeepAspectRatio))

        # initializes health
        h = Bar(self)
        h.set_max_val(1200)
        h.set_current_val(1200)
        self.set_health(h)

        # set signal
        self.s = NexusSignal()

        # set not damageable
        self.set_damageable(False)

        # allow responding to hover events
        self.setAcceptHoverEvents(True)

    def decrease_health(self, value):
        '''Overriding decrease health to emit a signal if it dies '''
        if not self.damageable:
            return
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
            self.setPixmap(QPixmap('./res/imgs/lol_nexus_1_red.png').
                           scaled(80, 80, Qt.KeepAspectRatio))

    def hoverLeaveEvent(self, event):
        '''event: QGraphicsSceneHoverEvent '''
        # change back pixmap
        if self.team == 2:
            self.setPixmap(QPixmap('./res/imgs/lol_nexus_1.png').
                           scaled(80, 80, Qt.KeepAspectRatio))
