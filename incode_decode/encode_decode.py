# -*- coding: utf-8 -*-
import numpy as np
import urllib
import cv2
import pickle
import base64
from time import time

#img = cv2.imread('../RES/lena.jpg')
img = cv2.imread('./road.jpg')
#img = cv2.imread('~/upload/road.jpg')

start = time()

# '.jpg'表示把当前图片img按照jpg格式编码，按照不同格式编码的结果不一样
img_encode = cv2.imencode('.jpg', img)[1]
img_base64 = base64.b64encode(img_encode)

encode_time = time() - start
start = time()

img2_encode = base64.b64decode(img_base64)
img2_array = np.fromstring(img2_encode, np.uint8)
img2 = cv2.imdecode(img2_array, cv2.IMREAD_COLOR)

decode_time = time() - start

#data_encode = np.array(img_encode)
#str_encode = data_encode.tostring()

print('image size: ', img.size)
print('image encode size: ', img_encode.size)
print('Encode time: {:.5f}, decode time: {:.5f}.'.format(encode_time, decode_time))

#image = cv2.imdecode(np.fromfile('img_encode.txt', dtype = np.uint8), -1)
cv2.imshow('Image_decode', img2)
cv2.waitKey()


