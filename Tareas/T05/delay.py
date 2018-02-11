from PyQt5.QtCore import QDateTime, QCoreApplication, QEventLoop


def delay(secs=1):

    dieTime = QDateTime.currentDateTime().addSecs(secs)
    while QDateTime.currentDateTime() < dieTime:
        QCoreApplication.processEvents(QEventLoop.AllEvents, 100)
