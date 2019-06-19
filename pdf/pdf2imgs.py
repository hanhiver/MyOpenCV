#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 16:18:35 2019

@author: dhan
"""
import PIL
import cv2 as cv
import numpy as np 
import pdf2image 


def pdf2img(pdf_file):
	images = pdf2image.convert_from_path(pdf_file)
	return images

def cut_image(image, threshold = 210, dilate_iteration = 20):
	# Convert image from RGB to Gray. 
	image_gray = cv.cvtColor(page, cv.COLOR_RGB2GRAY)

	# Using threshold to binaryzate the image. 
	image_bin = (image_gray, threshold, 255, cv.THRESH_BINARY)[1]

	# Reverse the image for dilate cut. 
	image_ones = np.ones(shape = image_bin.shape, dtype = np.uint8)
	image_revers = image_ones * 255 - image_bin

	# Dilate the image to separate chars clusters. 
	image_dilate = cv.dilate(page, None, iterations = dilate_iteration)

	# Find chars clusters. 
	contours, hierarchy = cv.findContours(image_dilate, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

	res_images = []

	for item in contours:
		image_zeros = np.zeros(shape = image_bin.shape, dtype = np.uint8)
		image_contour = cv.drawContours(image_zeros, [item], -1, 1, -1)
		res = image_contour * image_bin 
		res_images.append(res)

	return res_images




img = convert_from_path('./test1.pdf')
#img[0].save('test.png')


img = np.asarray(img[0])
page = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
page = cv.threshold(page, 210, 255, cv.THRESH_BINARY)[1]

full = np.ones(shape = page.shape, dtype = np.uint8) * 255
page = full - page 

page = cv.dilate(page, None, iterations = 20)

contours, hierarchy = cv.findContours(page, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

contour_img = cv.drawContours(img, contours, -1, 255, 3)

result = contour_img

cv.imwrite('test.png', result)

cv.imshow('PDF', result)
cv.waitKey()


