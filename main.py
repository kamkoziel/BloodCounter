# This Python file uses the following encoding: utf-8
import sys

from PyQt5.QtWidgets import QApplication
from widgets.MainWindow import App


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())