import os, sys, argparse, time, datetime
import queue
import multiprocessing 
import sched
import numpy as np
import cv2 
#from PIL import Image

class SchedRun():
    def __init__(self, func, args, init_func = None, init_args = {}, interval = 0.04, init_interval = 0.5):
        self.func = func
        self.args = args
        self.init_func = init_func
        self.init_args = init_args
        self.interval = interval
        self.init_interval = init_interval

        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.sub_process = multiprocessing.Process(target = self.wrap_process, args = {})
        self.sub_process_continue = True
        self.sub_process.start()

    def __del__(self):
        self.sub_process.join()

    def wrap_func(self):
        if self.sub_process_continue:
            self.scheduler.enter(self.interval, 1, self.wrap_func)
            self.sub_process_continue = self.func(*self.args)
        else:
            return

    def wrap_process(self):
        if self.init_func:
            self.init_func(*self.init_args)

        self.scheduler.enter(self.init_interval, 1, self.wrap_func) 
        self.scheduler.run()
        return

def init_show_windows():
    cv2.namedWindow("result", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("result", 640, 400)
    cv2.moveWindow("result", 100, 100)
    print('Init show windows finished. ')

def show_frame(input_queue, timeout = 3):
    try:
        frame = input_queue.get(timeout = timeout)
        
        cv2.imshow('result', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            return False
    except queue.Empty:
        print('Queue empty.')
        cv2.destroyAllWindows()
        return False

    return True

def main(input_file):
    frame_queue = multiprocessing.Queue()

    sched_run = SchedRun(func = show_frame, args = {frame_queue}, 
                         init_func = init_show_windows, 
                         interval = 0.035, 
                         init_interval = 0.5)

    vid = cv2.VideoCapture(input_file)

    if not vid.isOpened():
        raise IOError("Couldn't open webcam or video")

    video_FourCC    = int(vid.get(cv2.CAP_PROP_FOURCC))
    video_fps       = vid.get(cv2.CAP_PROP_FPS)
    video_size      = (int(vid.get(cv2.CAP_PROP_FRAME_WIDTH)),
                        int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    print("!!! TYPE:", type(input_file), type(video_FourCC), type(video_fps), type(video_size))
    print("!!! TYPE:", input_file, video_FourCC, video_fps, video_size)

    while True:
        got_a_frame, frame = vid.read()
        if type(frame) != type(None):
            frame_queue.put(frame)
        else:
            print('Video Finished.')
            break

if __name__ == '__main__':
    main('1_part.avi')




