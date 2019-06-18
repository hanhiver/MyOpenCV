import sys
import numpy as np 
import cv2 as cv


def main():
	if len(sys.argv) < 3:
		print("Please input the source image and destination image correctly. ")
		return

	src_file = sys.argv[1]
	dst_file = sys.argv[2]
	
	src_img = cv.imread(src_file)
	dst_img = cv.imread(dst_file)

	delta_img = cv.absdiff(src_img, dst_img)
	delta = delta_img.sum()

	print(delta)

	return delta


if __name__ == '__main__':
    delta = main()



