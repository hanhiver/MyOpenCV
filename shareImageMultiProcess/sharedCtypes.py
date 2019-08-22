#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 15:42:14 2019

Testing program that share the numpy array between different processes. 

@author: dhan
"""

import multiprocessing as mp
from multiprocessing.sharedctypes import RawArray
#from multiprocessing.sharedctypes import copy
import ctypes
import numpy as np
import cv2 as cv

def func(array):
    image = cv.imread('../RES/lena_color.png')
    
    src = np.ctypeslib.as_ctypes(image)
    size = ctypes.sizeof(array)
    
    # 子进程通过这样的方式将ndarray中的内容拷贝到共享内存中去。
    ctypes.memmove(array, src, size)


def main():
    
    image = cv.imread('../RES/lena_color.png')
    shape = image.shape
    
    temp = np.ones(shape = (image.size), dtype = np.ubyte)
    shared_array = RawArray(ctypes.c_ubyte, temp)
    
    
    p = mp.Process(target = func, args = (shared_array, ))
    p.start()
    p.join()
    
    
    result = np.array(shared_array, dtype = np.uint8)
    result = result.reshape(shape)
    
    print(result.shape)

    cv.namedWindow('Result')
    cv.imshow('Result', result)
    cv.waitKey(0)
    
    cv.destroyAllWindows()
    
if __name__ == '__main__':
    main()
    
