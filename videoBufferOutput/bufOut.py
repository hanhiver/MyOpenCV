import os, sys, argparse, time
import queue
import multiprocessing
import threading 
import numpy as np
import cv2 
from PIL import Image

def fill_buffer(buffer_queue, input_file):
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
            buffer_queue.put(frame)
        else:
            print('Video Finished.')
            break

def show_image(buffer_queue, fps = 15):
    cv2.namedWindow("result", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("result", 640, 400)
    cv2.moveWindow("result", 100, 100)
    
    while True:
        try:
            frame = buffer_queue.get(timeout = 1)
        except queue.Empty:
            print('Queue Empty. ')
            break

        print(frame.shape, type(frame))
        cv2.imshow('result', frame)
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break
        #time.sleep(1/fps)


def main():
    buffer_queue = multiprocessing.Queue()
    fill_process = multiprocessing.Process(target = fill_buffer, args = (buffer_queue, './1_part.avi'))
    show_process = multiprocessing.Process(target = show_image, args = (buffer_queue, ))

    fill_process.start()
    time.sleep(0.5)
    show_process.start()

    fill_process.join()
    show_process.join()

def main2(input_file):
    vid = cv2.VideoCapture(input_file)
    if not vid.isOpened():
        raise IOError("Couldn't open webcam or video")


    video_FourCC    = int(vid.get(cv2.CAP_PROP_FOURCC))
    video_fps       = vid.get(cv2.CAP_PROP_FPS)
    video_size      = (int(vid.get(cv2.CAP_PROP_FRAME_WIDTH)),
                        int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    print("!!! TYPE:", type(input_file), type(video_FourCC), type(video_fps), type(video_size))
    print("!!! TYPE:", input_file, video_FourCC, video_fps, video_size)
    print('\n')
    
    cv2.namedWindow("result", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("result", 640, 400)
    cv2.moveWindow("result", 100, 100)

    frame_index = 0

    while True:
        got_a_frame, frame = vid.read()
        if type(frame) != type(None):
            print('\tOne frame {:3}'.format(frame_index), frame.shape)
            frame_index += 1
            image = Image.fromarray(frame)
            result = np.asarray(image)
            cv2.imshow('result', result)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print('Video Finished.')
            break

    cv2.destroyAllWindows()


def main3(video_path):
    import cv2
    vid = cv2.VideoCapture(video_path)

    if not vid.isOpened():
        raise IOError("Couldn't open webcam or video")

    video_FourCC    = int(vid.get(cv2.CAP_PROP_FOURCC))
    video_fps       = vid.get(cv2.CAP_PROP_FPS)
    video_size      = (int(vid.get(cv2.CAP_PROP_FRAME_WIDTH)),
                        int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    cv2.namedWindow("result", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("result", 640, 400)
    cv2.moveWindow("result", 100, 100)

    q = queue.Queue()

    while True:
        return_value, frame = vid.read()
        if type(frame) != type(None):
            image = Image.fromarray(frame)
            result = np.asarray(image)
            time.sleep(0.1)
            q.put(result)
            result_queue = q.get()
            cv2.imshow("result", result_queue)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    
    cv2.destroyAllWindows()

def main4():
    process = multiprocessing.Process(target = main3, args = ('1s.mp4', ))
    process.start()
    process.join()

if __name__ == '__main__':
    main()
    #main2('1_part.avi')
    #main3('1_part.avi')

