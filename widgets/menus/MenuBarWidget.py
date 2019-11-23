from PyQt5.QtWidgets import QMenuBar,  QAction, QMenu
from widgets.MainWidget import MainWidget


class MenuBarWidget(QMenuBar):
    def __init__(self, mainWidget):
        super().__init__()
        self.setStyleSheet('''background: #393e46;
                                :hover{background: #232931;}''')
        self.mainWidget: MainWidget = mainWidget

        self.file = self.addMenu("File")
        self.file = self.addMenu("Edit")
        self.show = self.addMenu("Show")

        self.showFileTreeAct = QAction('Show file tree', shortcut="Ctrl+D", enabled=True, checkable=True, triggered=self.showFileTree)
        self.show.addAction(self.showFileTreeAct)


    def showFileTree(self):
        showFiles = self.showFileTreeAct.isChecked()
        self.mainWidget.tree.setHidden(showFiles)