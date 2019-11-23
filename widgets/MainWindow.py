from PyQt5 import QtGui, QtCore
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
        self.setStyleSheet('''        
        QMainWindow{
        background: #232931;
        color: #eeeeee;
        }
        QMenuBar{
        background: #393e46;
        color: #eeeeee;
        }
        QMenuBar::item:selected{
        background: #232931;
        color: #eeeeee;
        }
        QMenu{
        background: #393e46;
        color: #eeeeee;
        }
        QMenu::item:selected {
        background: #232931;
        }
        QWidget{
        color: #eeeeee;}
        
        QView{
        border: 1 1 1 1 #232931;
        }        
        QTreeView{
        background: #232931;
        color: #eeeeee;        
        border: 2px solid #393e46;
        }
        QHeaderView::section{
        background: #393e46;
        color: #eeeeee;
        }
        QSplitter::handle:horizontal{
        background: #4ecca3;
        }
        QStatusBar{
         background: #4ecca3;
         color:#393e46;
        }
        QMessageBox{
         background: #232931;         
        }
         QMessageBox QPushButton{
         background: #393e46;         
        }
        ''')
        self.setWindowIcon(QtGui.QIcon('img/DPC.png'))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setMenuBar(MenuBarWidget(mianWidget))
        self.statusBar().showMessage('Ready')
        self.setCentralWidget(mianWidget)


        self.show()

