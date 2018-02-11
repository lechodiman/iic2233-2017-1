from PyQt5.QtCore import QObject, pyqtSignal


class ChampionSignal(QObject):
    '''This signal will be connected to champion died function '''
    died = pyqtSignal()
