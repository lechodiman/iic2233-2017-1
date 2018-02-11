from PyQt5.QtWidgets import (QWidget, QFrame, QApplication, QMainWindow,
                             QGraphicsScene, QGraphicsRectItem,
                             QGraphicsView, QGraphicsItem, QGraphicsTextItem, QGraphicsPixmapItem,
                             QGraphicsPolygonItem)
from PyQt5.QtCore import Qt, QTimer, QObject, QUrl, QPointF, QLineF, pyqtSignal, QRectF
from PyQt5.QtGui import QFont, QPixmap, QImage, QBrush, QPolygonF, QCursor, QPen
from PyQt5.QtTest import QTest
from math import sin, cos, pi

from DynamicGameObject import DynamicGameObject
from Bar import Bar
from Bullet import Bullet
from Minion import Minion
from BigMinion import BigMinion
from PlayerChampion import PlayerChampion
from ChampionSignal import ChampionSignal


class ComputerChampion(DynamicGameObject):

    def __init__(self):
        super().__init__()
        # initialize cooldown time and ulti available
        self.ulti_available = True
        self.cooldown = 1000

        # set animations
        self.current_frame = 0
        self.sprite_image = QPixmap()

        # had to set a pixmap so the health bar works correctly
        self.setPixmap(QPixmap('./res/imgs/enemy_3.png').scaled(50, 50, Qt.KeepAspectRatio))
        self.setTransformOriginPoint(25, 25)

        # create a timer to change the frame
        self.sprite_timer = QTimer()
        self.sprite_timer.timeout.connect(self.nextFrame)

        # ulti cooldown timer
        self.ulti_cooldown_timer = QTimer()
        self.ulti_cooldown_timer.timeout.connect(self.set_ulti_available)
        self.ulti_cooldown_timer.setSingleShot(True)

        # ulti timer
        self.execute_ulti_timer = QTimer()
        self.execute_ulti_timer.timeout.connect(self.execute_ulti)
        self.execute_ulti_timer.start(10000)

        # set signal
        self.s = ChampionSignal()

    def set_ulti_available(self):
        self.ulti_available = True

    def set_cooldown(self, value):
        self.cooldown = value

    def set_sprite_image(self, pixmap):
        self.sprite_image = pixmap

    def nextFrame(self):
        self.current_frame += 64
        if self.current_frame >= 512:
            self.current_frame = 0
        self.update(-10, -10, 64, 64)

    def boundingRect(self):
        return QRectF(-10, -10, 64, 64)

    def paint(self, painter, option, widget):
        # draw one of the frames of the player
        painter.drawPixmap(-10, -10, self.sprite_image, self.current_frame,
                           0, 64, 64)

    def move_forward(self):
        '''Overwritting move forward so it changes the sprite '''
        if not self.has_target:
            self.nextFrame()
        super().move_forward()

    def ulti(self):
        return

    def execute_ulti(self):
        if not self.scene():
            return

        if self.ulti_available:
            self.ulti()

    def decrease_health(self, value):
        '''Overriding decrease health to emit a signal if it dies '''
        if not self.damageable:
            return

        self.health.decrement(value)

        if self.health.get_current_val() <= 0:
            self.s.died.emit()
            self.scene().removeItem(self)
            del self


class ComputerMage(ComputerChampion, BigMinion):
    def __init__(self):
        super().__init__()
        # graphics
        self.set_sprite_image(QPixmap('./res/imgs/player-move.png'))

        # set specs
        h = Bar(self)
        h.set_max_val(500)
        h.set_current_val(500)
        self.set_health(h)

        self.set_speed(5)
        self.set_attack(5)
        self.set_range(100)
        self.set_cooldown(30000)

        self.items_freezed = []

    def ulti(self):
        scene_items = self.scene().items()
        self.items_freezed = []

        # freeze items
        for i in scene_items:
            if hasattr(i, 'team') and i.team != self.team and isinstance(i, DynamicGameObject):
                if hasattr(i, 'wasd_timer') and i.wasd_timer.isActive():
                    i.wasd_timer.stop()
                    self.items_freezed.append(i)
                if i.move_timer.isActive() or i.damage_timer.isActive():
                    if i.move_timer.isActive():
                        i.move_timer.stop()
                    if i.damage_timer.isActive():
                        i.damage_timer.stop()
                    self.items_freezed.append(i)

        # Unfreeze
        self.unfreeze_timer = QTimer()
        self.unfreeze_timer.timeout.connect(self.unfreeze)
        self.unfreeze_timer.setSingleShot(True)
        self.unfreeze_timer.start(5000)

        self.ulti_available = False

        self.ulti_cooldown_timer.start(self.cooldown)

    def unfreeze(self):
        for i in self.items_freezed:
            if not isinstance(i, PlayerChampion):
                i.move_timer.start(1000 / 30)
                i.damage_timer.start(1000)
            else:
                i.wasd_timer.start(1000 / 30)


class ComputerTroll(ComputerChampion, Minion):
    def __init__(self):
        super().__init__()
        # graphics
        self.set_sprite_image(QPixmap('./res/imgs/troll-move.png'))

        # set specs
        h = Bar(self)
        h.set_max_val(666)
        h.set_current_val(666)
        self.set_health(h)

        self.set_speed(3)
        self.set_attack(5)
        self.set_range(40)
        self.set_cooldown(40000)

    def ulti(self):
        scene_items = self.scene().items()

        for i in scene_items:
            if (isinstance(i, Minion) or isinstance(i, BigMinion)) and i.team != self.team:
                this_line = QLineF(self.pos(), i.pos())
                if this_line.length() <= 150:
                    this_line.setLength(150)
                    i.setPos(i.x() + this_line.dx(), i.y() + this_line.dy())
            elif (i.__class__.__name__ == 'Tower' or i.__class__.__name__ == 'Nexus' or
                    i.__class__.__name__ == 'Inhibitor') and i.team != self.team:
                this_line = QLineF(self.pos(), i.pos())
                if this_line.length() <= 150:
                    i.decrease_health(100)

        self.ulti_available = False
        self.ulti_cooldown_timer.start(self.cooldown)


class ComputerOgrillion(ComputerChampion, BigMinion):
    def __init__(self):
        super().__init__()
        super().__init__()
        # graphics
        self.set_sprite_image(QPixmap('./res/imgs/ogrillion-move.png'))

        # set specs
        h = Bar(self)
        h.set_max_val(700)
        h.set_current_val(700)
        self.set_health(h)

        self.set_speed(5)
        self.set_attack(5)
        self.set_range(100)
        self.set_cooldown(10000)

    def ulti(self):
        # shots 5 bullets simultaneously
        bullet_1 = Bullet(self)
        bullet_2 = Bullet(self)
        bullet_3 = Bullet(self)
        bullet_4 = Bullet(self)
        bullet_5 = Bullet(self)

        bullet_1.set_damage(30)
        bullet_2.set_damage(30)
        bullet_3.set_damage(30)
        bullet_4.set_damage(30)
        bullet_5.set_damage(30)

        bullet_1.setPos(self.x() + 25, self.y() + 25)
        bullet_2.setPos(self.x() + 25, self.y() + 25)
        bullet_3.setPos(self.x() + 25, self.y() + 25)
        bullet_4.setPos(self.x() + 25, self.y() + 25)
        bullet_5.setPos(self.x() + 25, self.y() + 25)

        bullet_1.setRotation(self.rotation() - 90)
        bullet_2.setRotation(self.rotation() - 90 + 10)
        bullet_3.setRotation(self.rotation() - 90 - 10)
        bullet_4.setRotation(self.rotation() - 90 + 20)
        bullet_5.setRotation(self.rotation() - 90 - 20)

        self.scene().addItem(bullet_1)
        self.scene().addItem(bullet_2)
        self.scene().addItem(bullet_3)
        self.scene().addItem(bullet_4)
        self.scene().addItem(bullet_5)

        self.ulti_available = False
        self.ulti_cooldown_timer.start(self.cooldown)
