from unittest import TestCase

from features.Segementation import Segmentation
from features.Segmented_Image import Segmented_image


class TestSegmented_image(TestCase):
    def test_ConvertToHSV(self):
        image = Segmented_image()
        image.SetImage('C:\\Users\\kkozi\\Desktop\\BPC.jpg')
        image.ConvertToHSV()
        segmented_img = Segmentation(image)
        segmented_img.showCanal(1)

    def test_saveAsTif(self):
        image = Segmented_image()
        image.SetImage('C:\\Users\\kkozi\\Documents\\WORKSPACE\\pomwj_projekt\\data\\NPC\\NPC_1.JPG')
        image.ConvertToHSV()
        image.SaveAsTif('C:\\Users\\kkozi\\Documents\\WORKSPACE\\pomwj_projekt\\data\\NPC\\NPC_1.tif')

    def test_saveCatalogAsTif(self):
        import os
        path = "C:\\Users\\kkozi\\Documents\\WORKSPACE\\pomwj_projekt\\data\\BPC"
        listaPlikow = list(os.listdir(path = path))
        for file in listaPlikow:
            fileName = file.split('.')
            newname = fileName[0]
            if fileName[1] != 'tif':
                image = Segmented_image()
                image.SetImage('C:\\Users\\kkozi\\Documents\\WORKSPACE\\pomwj_projekt\\data\\BPC\\' + file)
                image.ConvertToHSV()
                image.SaveAsTif('C:\\Users\\kkozi\\Documents\\WORKSPACE\\pomwj_projekt\\data\\BPC\\' + newname + '.tif')