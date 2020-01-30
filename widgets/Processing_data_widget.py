import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QLabel, QGroupBox, QSpinBox
from PyQt5.QtWidgets import QPushButton

from features.Segmented_Image import Segmented_image
from widgets.Param_label import Param_label

class Processing_data_widget(QWidget):
    def __init__(self):
        super().__init__()


        self.setMinimumWidth(200)
        self.initUI()

    def initUI(self):
        #File info labels
        self.fileNameLabel = Param_label()
        self.filePathLabel = Param_label()
        self.fileExtLabel = Param_label()
        self.imageColorTypeLabel = Param_label()
        self.fileNameLabel.setText('file_name')
        self.filePathLabel.setText('file_path')
        self.fileExtLabel.setText('file_extension')
        self.imageColorTypeLabel.setText('image color type')

        file_layout = QVBoxLayout()
        file_layout.addWidget(QLabel("File name: "))
        file_layout.addWidget(self.fileNameLabel)
        file_layout.addWidget(QLabel("Path to file: "))
        file_layout.addWidget(self.filePathLabel)
        file_layout.addWidget(QLabel("File extesion: "))
        file_layout.addWidget(self.fileExtLabel)
        file_layout.addWidget(QLabel("Image color type: "))
        file_layout.addWidget(self.imageColorTypeLabel)

        proces_group = QGroupBox("Processing file")
        proces_group.setLayout(file_layout)
        proces_group.setMaximumHeight(300)

        #Segmentations params
        self.min_object_size_SBox = QSpinBox()
        self.min_object_size_SBox.setMinimum(100)
        self.min_object_size_SBox.setMaximum(100000)
        self.min_object_size_SBox.setValue(10000)
        self.threshold_down_SBox = QSpinBox()
        self.threshold_down_SBox.setMinimum(0)
        self.threshold_down_SBox.setMaximum(255)
        self.threshold_down_SBox.setValue(170)
        self.threshold_up_SBox = QSpinBox()
        self.threshold_up_SBox.setMinimum(0)
        self.threshold_up_SBox.setMaximum(255)
        self.threshold_up_SBox.setValue(255)

        params_layout = QVBoxLayout()
        params_layout.addWidget(QLabel("Minimum cell size: "))
        params_layout.addWidget(self.min_object_size_SBox)
        params_layout.addWidget(QLabel("Threshold down: "))
        params_layout.addWidget(self.threshold_down_SBox)
        params_layout.addWidget(QLabel("Threshold up: "))
        params_layout.addWidget(self.threshold_up_SBox)

        params_group = QGroupBox("Segmentation params")
        params_group.setLayout(params_layout)

        self.convert_btn = QPushButton("Convert to HSV coloring")
        self.convert_btn.setDisabled(True)
        self.process_btn = QPushButton("Make segmentation")
        self.process_btn.setDisabled(True)

        #Results labels
        self.cell_num_result = Param_label()
        result_layout = QVBoxLayout()
        result_layout.addWidget(QLabel('Number of cells: '))
        result_layout.addWidget(self.cell_num_result)

        result_group = QGroupBox("Result")
        result_group.setLayout(result_layout)
        result_group.setMaximumHeight(300)

        #Main layout
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop | Qt.AlignLeft )
        layout.addWidget(proces_group)
        layout.addWidget(params_group)
        layout.addWidget(self.convert_btn)
        layout.addWidget(self.process_btn)
        layout.addWidget(result_group)


    def SetFileNameLabel(self, text):
        self.fileNameLabel.setText(text)

    def SetFilePathLabel(self, text):
        self.filePathLabel.setText(text)

    def SetFileExtLabel(self, text):
        self.fileExtLabel.setText(text)

    def SetImageColorTypeLabel(self, text):
        self.imageColorTypeLabel.setText(text)

    def SetFileParams(self, path: str, colorType: str):
        filename, file_extension = os.path.splitext(path)
        self.SetFileNameLabel(os.path.basename(path))
        self.SetFilePathLabel(os.path.abspath(path))
        self.SetFileExtLabel(file_extension)
        self.SetImageColorTypeLabel(colorType)

    def SetConvertBtnActive(self):
        self.convert_btn.setDisabled(False)

    def SetConvertBtnDisactive(self):
        self.convert_btn.setDisabled(True)

    def SetCellsNumResult(self, num:int = 0):
        self.cell_num_result.setText(str(num))

    def GetMinObjSize(self):
        return self.min_object_size_SBox.value()

    def GetThrDown(self):
        return self.threshold_down_SBox.value()

    def GetThrUp(self):
        return self.threshold_up_SBox.value()

