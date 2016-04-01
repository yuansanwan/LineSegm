import cv2
import numpy as np
import peakutils


class LineLocalization:

    def __init__(self):
        pass

    def localize(self, im):
        # invert bw image
        im = self.invert(im)
        # execute projection profile analysis to localize lines of text
        peaks = self.projection_analysis(im)
        # compute the valley bewteen each pair of consecutive peaks
        indexes = []
        for i in range(0, len(peaks)-1):
            dist = (peaks[i+1] - peaks[i]) / 2
            middle = peaks[i] + dist
            indexes.append(middle)

        return indexes

    def invert(self, im):
        im = abs(255 - im)
        im = im / 255

        return im

    def projection_analysis(self, im):
        # compute the ink density histogram (sum each rows)
        hist = cv2.reduce(im, 1, cv2.REDUCE_SUM, dtype=cv2.CV_32F)
        hist = hist.ravel()
        # find peaks withing the ink density histogram
        max_hist = max(hist)
        mean_hist = np.mean(hist)
        thres_hist = mean_hist / max_hist
        peaks = peakutils.indexes(hist, thres=thres_hist, min_dist=60)
        # find peaks that are too high
        mean_peaks = np.mean(hist[peaks])
        std_peaks = np.std(hist[peaks])
        thres_peaks_high = mean_peaks + 1.5*std_peaks
        thres_peaks_low = mean_peaks - 3*std_peaks
        peaks = peaks[np.logical_and(hist[peaks] < thres_peaks_high,
                                     hist[peaks] > thres_peaks_low)]

        return peaks
