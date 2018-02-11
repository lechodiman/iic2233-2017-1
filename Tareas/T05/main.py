from Game import Game
from PyQt5.QtWidgets import QApplication
import sys


def main():
    app = QApplication(sys.argv)
    g = Game()
    g.show()
    g.display_main_menu()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
