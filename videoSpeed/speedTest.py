#!/usr/bin/env python
#! --*-- coding:utf-8 --*--
import cv2
import time
 
if __name__ == '__main__' :
    # 启动默认相机
    video = cv2.VideoCapture(0);
     
    # 获取 OpenCV version
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
    
    # 对于 webcam 不能采用 get(CV_CAP_PROP_FPS) 方法 
    # 而是：
    if int(major_ver)  < 3 :
        fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
        print("Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps))
    else :
        fps = video.get(cv2.CAP_PROP_FPS)
        print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))
     
    # Number of frames to capture
    num_frames = 120;
    print("Capturing {0} frames".format(num_frames))
 
    # Start time
    start = time.time()
    # Grab a few frames
    for i in range(0, num_frames):
        ret, frame = video.read()
    # End time
    end = time.time()
 
    # Time elapsed
    seconds = end - start
    print("Time taken : {0} seconds".format(seconds))
 
    # 计算FPS，alculate frames per second
    fps  = num_frames / seconds;
    print("Estimated frames per second : {0}".format(fps))
 
    # 释放 video
    video.release()
