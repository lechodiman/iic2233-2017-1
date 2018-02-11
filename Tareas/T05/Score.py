from PyQt5.QtWidgets import (QGraphicsTextItem)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class Score(QGraphicsTextItem):
    '''Class to keep track of the player's score '''

    def __init__(self, parent=None):
        super().__init__(parent)
        # initialize score value
        self.score = 0

        # draw the text
        self.setPlainText('Score: '.format(self.score))
        self.setDefaultTextColor(Qt.red)
        self.setFont(QFont('times', 16))

    def increase(self, value):
        self.score += value
        self.setPlainText('Score: '.format(self.score))

    def decrease(self, value):
        self.score -= value
        self.setPlainText('Score: '.format(self.score))

    def get_score(self):
        return self.score
