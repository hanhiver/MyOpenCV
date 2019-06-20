#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 16:18:35 2019

@author: dhan
"""
import sys
import PIL
import cv2 as cv
import numpy as np 
import pdf2image 

# Convert the pdf to images. 
# pdf_file: path to the pdf file. 
# return: images in opencv format, 1 page for 1 image. 
def pdf2img(pdf_file):
	images = pdf2image.convert_from_path(pdf_file)

	res_images = []

	for image in images:
		res = np.asarray(image)
		res_images.append(res)

	return res_images

# Cut one image to different chars clusters. 
# image: input image, opencv format. 
# threshold: threshold to convert identify the chars in the image. Default value 210.  
# char_distence: distences (pixels) between chars will be consider as one cluster. Default value 15. 
def cut_image(image, threshold = 210, char_distence = 15):
	# Convert image from RGB to Gray. 
	image_gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)

	# Using threshold to binaryzate the image. 
	image_bin = cv.threshold(image_gray, threshold, 255, cv.THRESH_BINARY)[1]

	# Reverse the image for dilate cut. 
	image_revers = ~ image_bin

	# Dilate the image to separate chars clusters. 
	image_dilate = cv.dilate(image_revers, None, iterations = char_distence)

	# Find chars clusters. 
	#contours, hierarchy = cv.findContours(image_dilate, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

	if cv.__version__[0] == '3':
		_, contours, hierarchy = cv.findContours(image_dilate, 
												 cv.RETR_EXTERNAL, 
												 cv.CHAIN_APPROX_SIMPLE)
	elif cv.__version__[0] == '4':
		contours, hierarchy = cv.findContours(image_dilate, 
											  cv.RETR_EXTERNAL, 
											  cv.CHAIN_APPROX_SIMPLE)

	res_images = []

	display = None

	for item in contours:
		image_zeros = np.zeros(shape = image_bin.shape, dtype = np.uint8)
		image_mask = cv.drawContours(image_zeros, [item], -1, 1, -1)

		res = ~ cv.copyTo(image_revers, image_mask)
		res_images.append(res)

	return res_images

def main():
	if len(sys.argv) < 2: 
		print('Please input correct pdf file name. ')
		return

	pdf_images = pdf2img(sys.argv[1])

	output_file = sys.argv[1].split('.')[0] + '_page_' + '%03d' + '_sec_' + '%03d' + '.jpg'

	page_index = 1
	for page in pdf_images:
		res_images = cut_image(page)

		sec_index = 1
		for image in res_images:
			cv.imwrite(output_file%(page_index, sec_index), image)
			sec_index += 1
		
		page_index += 1

	print('Job Done! Total %d pages. '%(page_index - 1))

if __name__ == '__main__':
	main()

