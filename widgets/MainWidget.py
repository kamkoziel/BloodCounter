from PyQt5.QtCore import QDir, Qt
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QSplitter, QMessageBox
from PyQt5.QtWidgets import QWidget, QLabel, QFileSystemModel, QTreeView
from PyQt5.QtGui import QPixmap, QImage

from dicom import DICOM, FileFormatError


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.left = 10
        self.top = 10
        self.width = 400
        self.height = 500
        self.leftPanelWidth = 250
        self.initUI()

    def initUI(self):
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.archive_label = QLabel(
            '''Active archive:
                AET:                   {0}
                ''' )
        self.user_label = QLabel(
            '''Active User:
                AEC:      {0}
               ''')

        self.archive_label.setMaximumHeight(40)
        self.user_label.setMaximumHeight(40)

        self.model = QFileSystemModel()
        self.model.setRootPath(r'C:\Users\kkozi\Documents\WORKSPACE\pomwj_projekt\data ')
        self.model.setReadOnly(True)
        tmpIdx = self.model.index(r'C:\Users\kkozi\Documents\WORKSPACE\pomwj_projekt\data')

        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.doubleClicked.connect(self.getSelectedImage)
        self.tree.setRootIndex(tmpIdx)
        self.tree.setHidden(False)

        self.img = QPixmap('data/bloodExpl.jpg')
        self.imgLabel = QLabel()
        self.imgLabel.setAlignment(Qt.AlignCenter)
        self.imgLabel.setContentsMargins(30,0,0,30)
        self.imgLabel.setStyleSheet("text-align: right;")
        self.imgLabel.setPixmap(self.img)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.tree)
        splitter.addWidget(self.imgLabel)

        labelsLayout = QHBoxLayout()
        labelsLayout.addWidget(self.archive_label)
        labelsLayout.addWidget(self.user_label)

        downLayout = QHBoxLayout()
        downLayout.addWidget(splitter)

        mainLayout = QVBoxLayout(self)
        mainLayout.addLayout(labelsLayout)
        mainLayout.addLayout(downLayout)

    def getSelectedImage(self, index):
        path = self.model.filePath(index)
        self.img = QPixmap.fromImage(QImage(path))
        self.imgLabel.setPixmap(self.img)
        try:
            DICOM.loadData(path)
        except FileFormatError as ex:
            print(ex)
            QMessageBox.information(self,
                                    'Format no supported',
                                    '{0}'.format(str(ex.message)),
                                    QMessageBox.Ok)

    def resizeEvent(self, event):
        self.img = self.img.scaled(self.imgLabel.width() *0.7, self.imgLabel.height()*0.7, Qt.KeepAspectRatio)
        self.imgLabel.setPixmap(self.img)
        self.imgLabel.resize(self.width*0.8, self.height*0.8)

