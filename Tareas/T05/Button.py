from PyQt5.QtWidgets import (QWidget, QFrame, QApplication, QMainWindow,
                             QGraphicsScene, QGraphicsRectItem,
                             QGraphicsView, QGraphicsItem, QGraphicsTextItem, QGraphicsPixmapItem,
                             QGraphicsPolygonItem)
from PyQt5.QtCore import Qt, QTimer, QObject, QUrl, QPointF, QLineF, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap, QImage, QBrush, QPolygonF, QCursor


class ButtonSignal(QObject):
    clicked = pyqtSignal()


class MenuButton(QGraphicsRectItem):

    def __init__(self, name, height=200, width=50, parent=None):
        '''name: str '''
        super().__init__(parent)
        # Set locked atribute
        self.locked = False

        # create my signal
        self.s = ButtonSignal()

        # draw the rect
        self.setRect(0, 0, height, width)

        # change color of rect
        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)
        brush.setColor(Qt.darkCyan)
        self.setBrush(brush)

        # draw the text
        self.text = QGraphicsTextItem(name, self)
        x_pos = self.rect().width() / 2 - self.text.boundingRect().width() / 2
        y_pos = self.rect().height() / 2 - self.text.boundingRect().height() / 2
        self.text.setPos(x_pos, y_pos)

        # allow responding to hover events
        self.setAcceptHoverEvents(True)

    def mousePressEvent(self, event):
        if not self.locked:
            self.s.clicked.emit()

    def hoverEnterEvent(self, event):
        '''event: QGraphicsSceneHoverEvent '''
        # change color to cyan
        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)
        brush.setColor(Qt.cyan)
        self.setBrush(brush)

    def hoverLeaveEvent(self, event):
        '''event: QGraphicsSceneHoverEvent '''
        # change color to dark cyan
        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)
        brush.setColor(Qt.darkCyan)
        self.setBrush(brush)

    def unlock(self):
        self.setOpacity(1)
        self.locked = False

    def lock(self):
        self.setOpacity(0.3)
        self.locked = True


class GameButton(MenuButton):

    def __init__(self, name):
        super().__init__(name)
        self.setOpacity(0.3)

    def hoverEnterEvent(self, event):
        self.setOpacity(1)
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setOpacity(0.3)
        super().hoverLeaveEvent(event)


class ChampionButton(QGraphicsPixmapItem):

    def __init__(self, champ_name):
        self.champ_name = champ_name
        super().__init__()
        self.setPixmap(QPixmap('./res/imgs/Champions/' + champ_name +
                               'Square.png').scaled(40, 40, Qt.KeepAspectRatio))
        self.s = ButtonSignal()

    def mousePressEvent(self, event):
        self.s.clicked.emit()
