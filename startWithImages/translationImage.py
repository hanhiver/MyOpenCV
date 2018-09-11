import numpy as np
import cv2

img = cv2.imread('lena.jpg', 0)
rows, cols = img.shape

# Set the translation matrix
# This will move the img to 100pix right and 50pix down
M = np.float32([[1, 0, 100], [0, 1, 50]])
dst = cv2.warpAffine(img, M, (cols, rows))

# Set the rotation matrix
# This will rotate the img to 75degree
M = cv2.getRotationMatrix2D(((cols-1)/2.0, (rows-1)/2.0), 75, 1)
dst = cv2.warpAffine(dst, M, (cols, rows))

cv2.imshow('img', dst)
cv2.waitKey(0)
cv2.destroyAllWindows()
