import numpy as np 
import cv2 as cv
import time
import argparse

def wsVideoPhase(input):
    time_stamp = time.time()

    #vid = cv.VideoCapture(input[0])
    vid = cv.VideoCapture(0)

    if not vid.isOpened():
        raise IOError("Couldn't open webcam or video: {}".format(input))
    
    vid.set(cv.CAP_PROP_FRAME_WIDTH, 800)
    vid.set(cv.CAP_PROP_FRAME_HEIGHT, 600)
    print(vid.get(cv.CAP_PROP_FPS))

    cv.namedWindow("result")
    #cv.resizeWindow("result", 800, 400)

    time_cur = time.time()
    print('\t[{:3.3f} ms]: 初始化完成. '.format((time_cur - time_stamp)*1000));
    time_stamp = time_cur

    while True:
        return_value, frame = vid.read()

        time_cur = time.time()
        print('\t[{:3.3f} ms]: 读取一帧. '.format((time_cur - time_stamp)*1000));
        time_stamp = time_cur

        if type(frame) != type(None):
            
            cv.imshow("result", frame)
            if cv.waitKey(1) & 0xFF == ord('q'):
                return False

            time_cur = time.time()
            print('\t[{:3.3f} ms]: 显示一帧. '.format((time_cur - time_stamp)*1000));
            time_stamp = time_cur
            
        else:
            break             

    cv.destroyAllWindows()


def main():

    parser = argparse.ArgumentParser()

    # 默认处理所有文件选项。
    parser.add_argument('input', type = str, default = None, nargs = '+',
                        help = 'Input files. ')

    FLAGS = parser.parse_args()

    if FLAGS.input:
        wsVideoPhase(input = FLAGS.input)

    else:
        print("See usage with --help.")


if __name__ == '__main__':
    main()


