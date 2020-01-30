from PyQt5.QtWidgets import QMenuBar, QAction, QMenu, QFileDialog

from features.Segementation import Segmentation
from features.Segmented_Image import Segmented_image
from widgets.MainWidget import MainWidget
import SimpleITK as sitk
import matplotlib.pyplot as plt

class MenuBarWidget(QMenuBar):
    def __init__(self, mainWidget):
        super().__init__()

        self.mainWidget: MainWidget = mainWidget

        self.file = self.addMenu("File")
        self.edit = self.addMenu("Edit")
        self.show = self.addMenu("Show")

        self.showFileTreeAct = QAction('Show file tree', shortcut="Ctrl+D", enabled=True, checkable=True, triggered=self.showFileTree)
        self.setDirect = QAction('Select main directory', triggered=self.setActiveDirectory)

        self.file.addAction(self.setDirect)
        self.show.addAction(self.showFileTreeAct)


    def showFileTree(self):
        showFiles = self.showFileTreeAct.isChecked()
        self.mainWidget.tree.setHidden(not showFiles)

    def setActiveDirectory(self):
        directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))

        self.mainWidget.model.setRootPath(directory)
        tmpIdx = self.mainWidget.model.index(directory)
        self.mainWidget.tree.setRootIndex(tmpIdx)

