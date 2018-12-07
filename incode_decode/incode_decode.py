# -*- coding: utf-8 -*-
import numpy as np
import urllib
import cv2

img = cv2.imread('../RES/lena.jpg')
# '.jpg'表示把当前图片img按照jpg格式编码，按照不同格式编码的结果不一样
img_encode = cv2.imencode('.jpg', img)[1]
# imgg = cv2.imencode('.png', img)

img_encode.tofile('img_encode.txt')
data_encode = np.array(img_encode)
str_encode = data_encode.tostring()

print(type(str_encode))

image = cv2.imdecode(np.fromfile('img_encode.txt', dtype = np.uint8), -1)
cv2.imshow('Image_decode', image)
cv2.waitKey()

"""
# 缓存数据保存到本地，以txt格式保存
with open('img_encode.txt', 'w') as f:
    f.write(str_encode)
    f.flush

with open('img_encode.txt', 'r') as f:
    str_encode = f.read()
"""
"""
nparr = np.fromstring(str_encode, np.uint8)
img_decode = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
cv2.imshow("img_decode", img_decode)
cv2.waitKey()
"""



"""
image = np.asarray(bytearray(str_encode), dtype="uint8")
image = cv2.imdecode(image, cv2.IMREAD_COLOR)
cv2.imshow('img_decode',image)
cv2.waitKey()
"""

