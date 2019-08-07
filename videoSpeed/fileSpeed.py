#!/usr/bin/env python
#! --*-- coding:utf-8 --*--
import cv2
import sys

if __name__ == '__main__' :
    
    if len(sys.argv) > 1:
        open_file = sys.argv[1]
    else:
        open_file = 0

    video = cv2.VideoCapture(open_file);
     
    # Find OpenCV version
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
     
    if int(major_ver)  < 3 :
        fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
        print("Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps))
    else :
        fps = video.get(cv2.CAP_PROP_FPS)
        print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))
    
    video.release() 
