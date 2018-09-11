import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('lena.jpg', 0)

#cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.imshow('image', img)
k = cv2.waitKey(0)

if k == 27:
    cv2.destroyAllWindows()
elif k == ord('i'):
    plt.imshow(img, cmp = 'gray', interpolation = 'bicubic')
    plt.xticks([]), plt.yticks([])
    plt.show()
elif k == ord('s'):
    cv2.imwrite('lenagray.jpg', img)
    cv2.destroyAllWindows()

    
