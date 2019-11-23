from medpy.io import *
import SimpleITK as sitk

class DICOM():
    def __init__(self):
        self.__data = []

    @staticmethod
    def loadData(name):
        reader = sitk.ImageFileReader()
        reader.SetImageIO("GDCMImageIO")
        reader.SetFileName(name)
        image = reader.Execute()
        array = sitk.GetArrayFromImage(image)
        return array

    def loadDataSet(self, name):
        return load(name)

    def getData(self):
        return self.__data