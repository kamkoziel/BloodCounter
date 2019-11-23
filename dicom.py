import os

from medpy.io import *
import SimpleITK as sitk


class FileFormatError(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class DICOM():
    def __init__(self):
        self.__data = []

    @staticmethod
    def loadData(pathToFile):
        reader = sitk.ImageFileReader()
        filename, file_extension = os.path.splitext(pathToFile)
        jpgFormats = ['.jpg', '.JPG', '.jpeg', '.JPEG']
        bmpFormats = ['.bmp', '.BMP' ]
        pngFormats = ['.png', '.PNG' ]

        if file_extension == '.dcm':
            reader.SetImageIO("GDCMImageIO")
        elif jpgFormats.count(file_extension) == 1:
            reader.SetImageIO("JPEGImageIO")
        elif bmpFormats.count(file_extension) == 1:
            reader.SetImageIO("BMPImageIO")
        elif pngFormats.count(file_extension) == 1:
            reader.SetImageIO("PNGImageIO")
        else:
            raise FileFormatError('Wrong file format', 'Files in format {0} is not supported'.format(file_extension) )

        reader.SetFileName(pathToFile)
        image = reader.Execute()
        array = sitk.GetArrayFromImage(image)
        return array


    def getData(self):
        return self.__data