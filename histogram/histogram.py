import cv2
import numpy
from matplotlib import pyplot
import time

img = cv2.imread('../RES/lena_color.jpg')
pyplot.hist(img.ravel(), 256, [0, 256])
#pyplot.show()

color = ('b', 'g', 'r')

for i, col in enumerate(color):
    histr = cv2.calcHist([img], [i], None, [256], [0, 256])
    pyplot.plot(histr, color = col)
    pyplot.xlim([0, 256])

pyplot.show()

