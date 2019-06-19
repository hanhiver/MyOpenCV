import sys
import numpy as np 
import cv2 as cv


# Caculate the differencial ratio of the two images. 
# Output should be a number of the differences. 0.05 means 5% differencial. 
def image_diff(src_img, dst_img):

	delta_img = cv.absdiff(src_img, dst_img)
	delta = delta_img.sum()

	src_sum = src_img.sum()
	result = delta / src_sum

	return result


def main():
	if len(sys.argv) < 3:
		print("Please input the source image and destination image correctly. ")
		return

	src_file = sys.argv[1]
	dst_file = sys.argv[2]
	
	src_img = cv.imread(src_file)
	dst_img = cv.imread(dst_file)

	result = image_diff(src_img, dst_img)
	
	print(result)


if __name__ == '__main__':
    delta = main()



