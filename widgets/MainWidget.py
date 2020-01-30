from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QSplitter, QMessageBox, QProgressDialog
from PyQt5.QtWidgets import QWidget, QLabel, QFileSystemModel, QTreeView
from PyQt5.QtGui import QPixmap, QImage
from widgets.Processing_data_widget import Processing_data_widget
from features.Segementation import Segmentation

from features.Segmented_Image import Segmented_image, FileFormatError


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.left = 10
        self.top = 10
        self.width = 400
        self.height = 500
        self.leftPanelWidth = 250
        self.processed_image : Segmented_image = None
        self.initUI()

    def initUI(self):
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.model = QFileSystemModel()
        self.model.setRootPath(r'C:\Users\kkozi\Documents\WORKSPACE\pomwj_projekt\data ')
        self.model.setReadOnly(True)
        tmpIdx = self.model.index(r'C:\Users\kkozi\Documents\WORKSPACE\pomwj_projekt\data')

        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.doubleClicked.connect(self.SetProcessedImage)
        self.tree.setRootIndex(tmpIdx)

        self.img = QPixmap(r'C:\Users\kkozi\Documents\WORKSPACE\pomwj_projekt\data\no_image.jpg')
        self.imgLabel = QLabel()
        self.imgLabel.setAlignment(Qt.AlignCenter)
        self.imgLabel.setContentsMargins(30,0,0,30)
        self.imgLabel.setStyleSheet("text-align: right; color: white;")
        self.imgLabel.setPixmap(self.img)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.tree)
        splitter.addWidget(self.imgLabel)

        self.processing_wdg = Processing_data_widget()
        self.processing_wdg.process_btn.clicked.connect(self.MakeSegmentation)

        downLayout = QHBoxLayout()
        downLayout.addWidget(splitter)
        downLayout.addWidget(self.processing_wdg)

        mainLayout = QVBoxLayout(self)
        mainLayout.addLayout(downLayout)

    def SetProcessedImage(self, index):
        try:
            path = self.model.filePath(index)
            self.processed_image = Segmented_image()
            self.processed_image.SetImage(path)
            self.processing_wdg.SetFileParams(path, self.processed_image.GetColorType())
            if self.ImgIsRGB():
                self.processing_wdg.SetConvertBtnActive()
                self.processing_wdg.convert_btn.clicked.connect(self.ConvertToHSV)
            else:
                self.processing_wdg.SetConvertBtnDisactive()
            self.processing_wdg.process_btn.setDisabled(False)
            self.ShowSelectedImage()

            if not self.processed_image.IsSetImage():
                QMessageBox.information(self, "Segmented_image Viewer", "Cannot load %s." % 'image')

        except FileFormatError as ex:
            QMessageBox.information(self,
                                    'Format no supported',
                                    '{0}'.format(str(ex.message)),
                                    QMessageBox.Ok)

    def ShowSelectedImage(self):
            self.img = QPixmap.fromImage(self.processed_image.GetQImageFromImage())
            self.img = self.img.scaled(self.imgLabel.width() * 0.9, self.imgLabel.height() * 0.9, Qt.KeepAspectRatio)
            self.imgLabel.setPixmap(self.img)
            self.imgLabel.resize(self.width * 0.95, self.height * 0.95)

    def MakeSegmentation(self):
        progress_dialog = QProgressDialog()
        segmentation = Segmentation(self.processed_image)
        progress_dialog.setValue(10)
        seg_img = segmentation.makeSegment(self.processing_wdg.GetMinObjSize(),
                                           self.processing_wdg.GetThrDown(),
                                           self.processing_wdg.GetThrUp())
        progress_dialog.setValue(30)
        self.processed_image = Segmented_image.FromSITKImage(seg_img)
        progress_dialog.setValue(50)
        self.processing_wdg.SetCellsNumResult(segmentation.GetCellsNum())
        progress_dialog.setValue(80)
        self.ShowSelectedImage()
        progress_dialog.setValue(100)
        progress_dialog.close()

    def resizeEvent(self, event):
        self.img = self.img.scaled(self.imgLabel.width() *0.9, self.imgLabel.height()*0.9, Qt.KeepAspectRatio)
        self.imgLabel.setPixmap(self.img)
        self.imgLabel.resize(self.width*0.95, self.height*0.95)

    def ImgIsRGB(self):
        if self.processed_image.colorType == 'RGB':
            return True
        else:
            return False

    def ConvertToHSV(self):
        progress_dialog = QProgressDialog()
        self.processing_wdg.SetConvertBtnDisactive()
        image = self.processed_image.ConvertToHSV()
        self.processed_image = Segmented_image.FromSITKImage(image)
        self.ShowSelectedImage()
        progress_dialog.close()



