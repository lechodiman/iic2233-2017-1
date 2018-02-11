from PyQt5.QtWidgets import (QWidget, QFrame, QApplication, QMainWindow,
                             QGraphicsScene, QGraphicsRectItem,
                             QGraphicsView, QGraphicsItem, QGraphicsTextItem, QGraphicsPixmapItem,
                             QGraphicsPolygonItem)
from PyQt5.QtCore import Qt, QTimer, QObject, QUrl, QPointF, QLineF, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap, QImage, QBrush, QPolygonF, QCursor


class StaticGameObject(QGraphicsPixmapItem):
    ''' Class to modelate the nexus, inhibitor, and tower'''

    def __init__(self, parent=None):
        super().__init__(parent)
        # initialize team
        self.team = 1
        self.health = None
        self.damageable = True

    def set_team(self, t):
        '''Defines the team of the object '''
        self.team = t

    def get_health(self):
        '''Returns the Bar object '''
        if self.health:
            return self.health

    def set_health(self, h):
        '''Bar h '''
        self.health = h
        self.health.update_bar()

    def decrease_health(self, value):
        if not self.damageable:
            return

        self.health.decrement(value)

        if self.health.get_current_val() <= 0:
            self.scene().removeItem(self)
            del self

    def restore_health(self):
        '''restores health completely'''
        self.health.increment(self.health.max_val - self.health.get_current_val())

    def get_origin(self):
        return self.mapToScene(self.transformOriginPoint())

    def is_damageable(self):
        '''I know this could be a property but i like the color of a function C: '''
        return self.damageable

    def set_damageable(self, b):
        self.damageable = b
