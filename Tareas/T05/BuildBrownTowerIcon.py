from PyQt5.QtWidgets import (QWidget, QFrame, QApplication, QMainWindow,
                             QGraphicsScene, QGraphicsRectItem,
                             QGraphicsView, QGraphicsItem, QGraphicsTextItem, QGraphicsPixmapItem,
                             QGraphicsPolygonItem)
from PyQt5.QtCore import Qt, QTimer, QObject, QUrl, QPointF, QLineF
from PyQt5.QtGui import QFont, QPixmap, QImage, QBrush, QPolygonF, QCursor
from Tower import Tower


class BuildBrownTowerIcon(QGraphicsPixmapItem):

    def __init__(self):
        super().__init__()
        self.build = None
        self.cursor = None
        # to detect mouse movement
        self.setPixmap(QPixmap('./res/imgs/towericon.png').scaled(40, 40))

    def mousePressEvent(self, event):
        if not self.build:
            self.build = BrownTower()
            self.set_cursor('./res/imgs/towericon.png')

    def mouseMoveEvent(self, event):
        print('inside move event of build icon')
        if self.cursor:
            self.cursor.setPos(event.pos())

    def set_cursor(self, filename):
        '''filename: str '''
        if self.cursor:
            self.scene().removeItem(self.cursor)
            del self.cursor

        self.cursor = QGraphicsPixmapItem(QPixmap(filename).scaled(40, 40))
        self.scene().addItem(self.cursor)
