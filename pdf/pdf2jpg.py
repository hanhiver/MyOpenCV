#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 16:18:35 2019

@author: dhan
"""
import PIL
import cv2 as cv
import numpy as np 
from pdf2image import convert_from_path

img = convert_from_path('./test1.pdf')
#img[0].save('test.png')

img = np.asarray(img[1])
page = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
page = cv.threshold(page, 210, 255, cv.THRESH_BINARY)[1]

full = np.ones(shape = page.shape, dtype = np.uint8) * 255
page = full - page 

page = cv.dilate(page, None, iterations = 15)

contours, hierarchy = cv.findContours(page, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

contour_img = cv.drawContours(img, contours, -1, 255, 3)

result = contour_img

cv.imwrite('test.png', result)

cv.imshow('PDF', result)
cv.waitKey()


