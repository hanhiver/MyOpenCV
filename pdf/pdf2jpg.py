#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 16:18:35 2019

@author: dhan
"""
import PIL
from pdf2image import convert_from_path

img = convert_from_path('./test.pdf')
img[0].save('test.png')
