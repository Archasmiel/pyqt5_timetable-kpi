import sys
from PyQt5 import QtWidgets, uic
from Ui import Ui


def main():
    app = QtWidgets.QApplication(sys.argv)
    win = Ui()
    app.exec_()


if __name__ == "__main__":
    main()
