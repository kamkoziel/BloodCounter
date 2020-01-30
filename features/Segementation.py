from features.Segmented_Image import Segmented_image
import SimpleITK as sitk
import numpy as np
import matplotlib.pyplot as plt

class Segmentation():
    def __init__(self, image: Segmented_image, canal = 0):
        self.image = image
        self._processed_img = image
        self.__canal = canal
        self.cells_num : int = 0

    def showCanal(self, canal=0):
        image = sitk.VectorIndexSelectionCast(self.image.image, canal)
        image_viewer = sitk.ImageViewer()
        image_viewer.SetTitle('Show canal')
        image_viewer.Execute(image)

    def showImage(self, image = None, title: str = 'image'):
        if image is None:
            image_viewer = sitk.ImageViewer()
            image_viewer.SetTitle(title)
            image_viewer.Execute(self._processed_img)
        else:
            image_viewer = sitk.ImageViewer()
            image_viewer.SetTitle(title)
            image_viewer.Execute(image)

    def makeSegment(self, min_size:int = 10000, threshold_down=170, thresholduold_up=255):
        self._processed_img = sitk.VectorIndexSelectionCast(self.image.image, 1)
        self._processed_img = self.makeOtsu()
        self._processed_img = sitk.Mask(sitk.VectorIndexSelectionCast(self.image.image, 1),self._processed_img, 0, 255)
        self._processed_img = self.makeMedian(radius=2)
        self._processed_img = self.makeBinary(self._processed_img, threshold_down=threshold_down, thresholduold_up=thresholduold_up)

        lab = sitk.ConnectedComponentImageFilter()
        lab.SetFullyConnected(False)
        relab = sitk.RelabelComponentImageFilter()
        relab.SetMinimumObjectSize(min_size)
        self._processed_img = lab.Execute(self._processed_img)
        self._processed_img = relab.Execute(self._processed_img)
        self._processed_img = self.makeBinary(self._processed_img, 1, 255)
        self._processed_img = self.makeErode()
        self._processed_img = self.makeCloseingRecostruction()
        self._processed_img = self.makeFill()
        self._processed_img = lab.Execute(self._processed_img)
        self._processed_img = relab.Execute(self._processed_img)
        self.cells_num = relab.GetNumberOfObjects()

        self._processed_img = sitk.LabelToRGB(self._processed_img)

        return self._processed_img

    def makeOtsu(self, image = None, num_bins = 100):
        otsu_filter = sitk.OtsuThresholdImageFilter()
        otsu_filter.SetInsideValue(255)
        otsu_filter.SetOutsideValue(0)
        otsu_filter.SetNumberOfHistogramBins(num_bins)
        if image is None:
            otsu_img = otsu_filter.Execute(self._processed_img)
        else:
            otsu_img = otsu_filter.Execute(image)

        return otsu_img

    def makeBinary(self,image = None,threshold_down =120, thresholduold_up = 135):
        binary_filter = sitk.BinaryThresholdImageFilter()
        binary_filter.SetLowerThreshold(threshold_down)
        binary_filter.SetUpperThreshold(thresholduold_up)
        binary_filter.SetInsideValue(255)
        binary_filter.SetOutsideValue(0)
        if image is None:
            bin_img = binary_filter.Execute(self._processed_img)
        else:
            bin_img = binary_filter.Execute(image)
        return bin_img

    def makeWatershed(self,image = None):
        segmentation_filter = sitk.MorphologicalWatershedImageFilter()
        segmentation_filter.SetLevel(255)
        segmentation_filter.MarkWatershedLineOff()
        segmentation_filter.SetFullyConnected(True)
        if image is None:
            seqmented_image = segmentation_filter.Execute(self._processed_img)
        else:
            seqmented_image = segmentation_filter.Execute(image)

        return seqmented_image

    def makeMedian(self, image = None, radius = 1):
        mean_filter = sitk.MeanImageFilter()
        mean_filter.SetRadius(radius)
        if image is None:
            mean_img = mean_filter.Execute(self._processed_img)
        else:
           mean_img = mean_filter.Execute(image)

        return mean_img

    def makeFill(self, image = None):

        fillHole_filter = sitk.GrayscaleFillholeImageFilter()
        fillHole_filter.FullyConnectedOn()
        if image is None:
            fillHole_img = fillHole_filter.Execute(self._processed_img)
        else:
            fillHole_img = fillHole_filter.Execute(image)

        return fillHole_img

    def makeLabelThreshold(self, image = None, n =5,threshold_down =0, thresholduold_up = 135):
        thr_filter = sitk.ThresholdImageFilter()
        thr_filter.SetLower(threshold_down)
        thr_filter.SetUpper(thresholduold_up)
        thr_filter.SetOutsideValue(0)
        thr_filter.SetNumberOfThreads(n)
        if image is None:
            thr_img = thr_filter.Execute(self._processed_img)
        else:
            thr_img = thr_filter.Execute(image)
        return thr_img

    def makeErode(self, image = None):
        if image is None:
            ero_filter = sitk.GrayscaleErodeImageFilter()

            ero_img = ero_filter.Execute(self._processed_img)
            return ero_img
        else:
            ero_filter = sitk.GrayscaleErodeImageFilter()
            ero_img = ero_filter.Execute(image)
            return ero_img

    def makeDilate(self, image = None):
        if image is None:
            dilate_filter = sitk.GrayscaleDilateImageFilter()

            dilate_img = dilate_filter.Execute(self._processed_img)
            return dilate_img
        else:
            dilate_filter = sitk.GrayscaleDilateImageFilter()
            dilate_img = dilate_filter.Execute(image)
            return dilate_img

    def makeClosing(self, image = None):
        close_filter = sitk.ClosingByReconstructionImageFilter()
        if image is None:
            close_img = close_filter.Execute(self._processed_img)
        else:
            close_img = close_filter.Execute(image)

        return close_img

    def makeShapeLabel(self,image = None):
        if image is None:
            shapeLabel_filter = sitk.LabelShapeStatisticsImageFilter()
            shapeLabel_filter.SetBackgroundValue(0)
            shapeLabel_filter.SetComputePerimeter()
            shapeLabel_img = shapeLabel_filter.Execute(self._processed_img)
            return shapeLabel_img
        else:
            shapeLabel_filter = sitk.LabelShapeStatisticsImageFilter()
            shapeLabel_img = shapeLabel_filter.Execute(image)
            return shapeLabel_img

    def makeSigned(self,image = None):
        if image is None:
            sig_filter = sitk.SignedMaurerDistanceMapImageFilter()
            sig_filter.SetBackgroundValue(0)

            sig_img = sig_filter.Execute(self._processed_img)
            return sig_img

        else:
            sig_filter = sitk.SignedMaurerDistanceMapImageFilter()
            sig_img = sig_filter.Execute(image)
            return sig_img

    def makeCloseingRecostruction(self, image = None):
        closeReco_filter = sitk.ClosingByReconstructionImageFilter()

        if image is None:
            sig_img = closeReco_filter.Execute(self._processed_img)
        else:
            sig_img = closeReco_filter.Execute(image)

        return sig_img

    def GetCellsNum(self):
        return self.cells_num
