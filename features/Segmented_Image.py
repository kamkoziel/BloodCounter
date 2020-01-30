import os
import SimpleITK as sitk
import vtk
from PyQt5.QtGui import QImage
import numpy as np
import colorsys


class FileFormatError(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class Segmented_image():
    def __init__(self, *args):
        super().__init__(*args)
        self.colorType = None
        self.image = None

    def IsSetImage(self):
        if self.image is not None:
            return True
        else:
            return False

    def SetImage(self, pathToFile: str):
        reader = sitk.ImageFileReader()
        filename, file_extension = os.path.splitext(pathToFile)
        jpgFormats = ['.jpg', '.JPG', '.jpeg', '.JPEG']
        bmpFormats = ['.bmp', '.BMP']
        pngFormats = ['.png', '.PNG']
        tifFormats = ['.tif', '.TIF', '.tiff', '.TIFF']

        if file_extension == '.dcm':
            reader.SetImageIO("GDCMImageIO")
        elif jpgFormats.count(file_extension) == 1:
            reader.SetImageIO("JPEGImageIO")
            self.colorType = 'RGB'
        elif bmpFormats.count(file_extension) == 1:
            reader.SetImageIO("BMPImageIO")
            self.colorType = 'RGB'
        elif pngFormats.count(file_extension) == 1:
            reader.SetImageIO("PNGImageIO")
            self.colorType = 'RGB'
        elif tifFormats.count(file_extension) == 1:
            reader.SetImageIO("TIFFImageIO")
            self.colorType = 'HSV'
        else:
            raise FileFormatError('Wrong file format', 'Files in format {0} are not supported'.format(file_extension))

        reader.SetFileName(pathToFile)
        self.image = reader.Execute()

        return self.image

    def GetImgArray(self):
        if self.image is not None:
            array = sitk.GetArrayFromImage(self.image)
            return array
        else:
            return False

    def GetColorType(self):
        return self.colorType

    def GetQImageFromImage(self):
        imgAsArray = sitk.GetArrayFromImage(self.image)
        imgAsQImage = QImage(imgAsArray, imgAsArray.shape[1], imgAsArray.shape[0], QImage.Format_RGB888)

        return imgAsQImage

    def ConvertToHSV(self, canal = 1):
        imgArr = sitk.GetArrayFromImage(self.image)
        img_shape = imgArr.shape

        for x in range(0,img_shape[0]-1):
            for y in range(0,img_shape[1]-1):
                k= colorsys.rgb_to_hsv(imgArr[x][y][0],imgArr[x][y][1],imgArr[x][y][2])
                c = [k[0]*255,k[1]*255,k[2]]
                imgArr[x][y] = c

        self.image = sitk.GetImageFromArray(imgArr, isVector= True)
        self.colorType = 'HSV'
        return self.image

    def SaveAsTif(self, name : str):
        writer = sitk.ImageFileWriter()
        writer.SetFileName(name + '.tif')
        writer.Execute(self.image)

    def __rgb2hsv(self, r, g, b):
        r, g, b = r / 255.0, g / 255.0, b / 255.0
        mx = max(r, g, b)
        mn = min(r, g, b)
        df = mx - mn
        if mx == mn:
            h = 0
        elif mx == r:
            h = (60 * ((g - b) / df) + 360) % 360
        elif mx == g:
            h = (60 * ((b - r) / df) + 120) % 360
        elif mx == b:
            h = (60 * ((r - g) / df) + 240) % 360
        if mx == 0:
            s = 0
        else:
            s = (df / mx) * 100
        v = mx * 100
        cell = np.array([h, s, v])
        return cell

    @staticmethod
    def FromSITKImage(image: sitk.Image, colorType: str = 'HSV'):
        img = Segmented_image()
        img.image = image
        img.colorType = colorType

        return img
