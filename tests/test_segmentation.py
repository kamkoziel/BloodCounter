import unittest
from unittest import TestCase
from features.Segementation import Segmentation
from features.Segmented_Image import Segmented_image
import SimpleITK as sitk
import matplotlib.pyplot as plt


class TestSegmentation(TestCase):
    def test_makeSegment(self):
        image = Segmented_image()
        image.SetImage('C:\\Users\\kkozi\\Documents\\WORKSPACE\\pomwj_projekt\\data\\NPC\\NPC_3.tif')
        segmented_img = Segmentation(image,1)
        test_img = segmented_img.makeSegment()
        segmented_img.showImage(title = 'Binared image')

    def test_showCanal(self):
        image = Segmented_image()
        image.SetImage('C:\\Users\\kkozi\\Documents\\WORKSPACE\\pomwj_projekt\\data\\NPC\\NPC_3.tif')
        segmented_img = Segmentation(image)
        segmented_img.showCanal(1)

if __name__ == '__main__':
    unittest.main()


