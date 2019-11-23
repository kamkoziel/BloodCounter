from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow
from widgets.MainWidget import MainWidget
from widgets.menus.MenuBarWidget import MenuBarWidget



class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.left = 40
        self.top = 80
        self.width=800
        self.height=650
        self.title = 'POMwJO Project - Blood elements counter'

        self.initUI()

    def initUI(self):
        mianWidget = MainWidget()
        self.setStyleSheet("background: #232931; color: #eeeeee")
        self.setWindowIcon(QtGui.QIcon('img/DPC.png'))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setMenuBar(MenuBarWidget(mianWidget))
        self.statusBar().showMessage('Ready')
        self.setCentralWidget(mianWidget)


        self.show()

