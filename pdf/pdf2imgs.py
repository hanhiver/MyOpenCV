#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 16:18:35 2019

@author: dhan
"""
import sys
import os
import argparse
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
# padding: padding each block image with padding pixels in both width and length.
# return: 
#       1. rect: (x, y, w, h) of each block. 
#       2. res_images: list of the block images.  
def cut_image(image, threshold = 210, char_distence = 15, padding = 30):
	# Convert image from RGB to Gray. 
	image_gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)

	# Using threshold to binaryzate the image. 
	image_bin = cv.threshold(image_gray, threshold, 255, cv.THRESH_BINARY)[1]

	# Reverse the image for dilate cut. 
	image_revers = ~ image_bin

	# Dilate the image to separate chars clusters. 
	image_erode = cv.erode(image_revers, None, iterations = 1)
	image_dilate = cv.dilate(image_erode, None, iterations = char_distence)

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

	res_rects = []
	res_images = []

	for item in contours:

		#image_zeros = np.zeros(shape = image_bin.shape, dtype = np.uint8)
		#image_mask = cv.drawContours(image_zeros, [item], -1, 1, -1)
		
		rect = cv.boundingRect(item)
		(x, y, w, h) = rect 
		
		# init a return block with blank padding. 
		res = np.full((h + padding*2, w + padding*2, 3), 255, dtype = np.uint8)
		
		# cut a block from the original image. 
		block = image[y:y+h, x:x+w]

		# fill the block to the center of the return result. 
		res[padding:padding+h, padding:padding+w] = block

		#res = ~ cv.copyTo(image_revers, image_mask)
		res_rects.append(rect)
		res_images.append(res)

	return res_rects, res_images

def phase_pdf(pdf_file):

	pdf_images = pdf2img(pdf_file)

	filename = pdf_file.split('/')[-1].split('.')[0]

	os.mkdir(filename)
	os.chdir(filename)

	output_file = 'page_' + '%03d' + '_sec_' + '%03d' + '_POS_%d_%d'+ '.jpg'

	page_index = 1
	for page in pdf_images:
		(res_rects, res_images) = cut_image(page)

		sec_index = 1
		for image in res_images:
			cv.imwrite(output_file%(page_index, 
									sec_index, 
									res_rects[sec_index-1][0], 
									res_rects[sec_index-1][1]), 
				       image)
			
			sec_index += 1
		
		page_index += 1

	os.chdir('../')

	print('Job Done! Total %d pages. '%(page_index - 1))

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('input', type = str, default = None, nargs = '+',
                        help = 'Input files. ')

    FLAGS = parser.parse_args()

    if FLAGS.input:
    	for item in FLAGS.input:
        	phase_pdf(item)
    else:
        print("See usage with --help.")


if __name__ == '__main__':
	main()

