from PyQt5 import QtGui, QtCore, Qt
from PyQt5.QtWidgets import QMainWindow
from widgets.MainWidget import MainWidget
from widgets.menus.MenuBarWidget import MenuBarWidget

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.left = 40
        self.top = 80
        self.width=500
        self.height=400
        self.title = 'POMwJO Project - Blood elements counter'

        self.initUI()

    def initUI(self):
        mianWidget = MainWidget()
        self.setStyleSheet(self.getStyle())
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setMenuBar(MenuBarWidget(mianWidget))
        self.statusBar().showMessage('Let\'s count')
        self.setCentralWidget(mianWidget)

        self.show()

    def getStyle(self):
        css_file = open('style.css', 'r')
        style = css_file.read()

        return style