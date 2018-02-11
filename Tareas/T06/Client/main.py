import sys
from ClientUI import Game
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":

    app = QApplication(sys.argv)
    app.setApplicationName('Progra - Pop')

    main = Game()
    main.show()

    sys.exit(app.exec_())
