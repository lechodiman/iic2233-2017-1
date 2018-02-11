from PyQt5.QtWidgets import (QWidget, QFrame, QApplication, QMainWindow,
                             QGraphicsScene, QGraphicsRectItem,
                             QGraphicsView, QGraphicsItem, QGraphicsTextItem, QGraphicsPixmapItem,
                             QGraphicsPolygonItem)
from PyQt5.QtCore import Qt, QTimer, QObject, QUrl, QPointF, QLineF
from PyQt5.QtGui import QFont, QPixmap, QImage, QBrush, QPolygonF, QCursor, QPen
from PlayerChampion import PlayerChampion
from Store import Store


class StoreIcon(QGraphicsPixmapItem):

    def __init__(self, parent=None):
        super().__init__()
        # bool to check if it is available
        self.available = False

        # set store gui
        self.gui = Store()

        # set graphics
        self.setPixmap(QPixmap('./res/imgs/blue_chest.png').scaled(80, 80, Qt.KeepAspectRatio))

        # create points vector
        points = [QPointF(1, 0), QPointF(2, 0), QPointF(3, 1),
                  QPointF(3, 2), QPointF(2, 3), QPointF(1, 3),
                  QPointF(0, 2), QPointF(0, 1)]

        # scale points
        SCALE_FACTOR = 100
        points = [p * SCALE_FACTOR for p in points]

        # create polygon
        self.polygon = QPolygonF(points)

        # create QGraphicsPolygonItem
        self.available_area = QGraphicsPolygonItem(self.polygon, self)
        self.available_area.setPen(QPen(Qt.DotLine))

        # move the polygon
        poly_center = QPointF(1.5 * SCALE_FACTOR, 1.5 * SCALE_FACTOR)
        poly_center = self.mapToScene(poly_center)
        store_center = QPointF(self.x() + 40, self.y() + 40)
        ln = QLineF(poly_center, store_center)
        self.available_area.setPos(self.x() + ln.dx(), self.y() + ln.dy())

        # connect the timer to acquire_champion
        self.timer = QTimer()
        self.timer.timeout.connect(self.acquire_champion)
        self.timer.start(1000)

    def mousePressEvent(self, event):
        if self.available:
            self.launch_store()

    def acquire_champion(self):
        colliding_items = self.available_area.collidingItems()

        found = False
        for item in colliding_items:
            if isinstance(item, PlayerChampion):
                self.set_available(True)
                found = True
        if not found:
            self.set_available(False)

    def set_available(self, bool_input):
        self.available = bool_input
        if not self.available and self.gui.isVisible():
            self.gui.close()

    def launch_store(self):
        self.gui.show()
