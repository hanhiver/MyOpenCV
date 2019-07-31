import math
import numpy as np 
import cv2 
import ctypes
import time
import argparse


"""
输入视频文件，处理视频文件。
input: 输入的视频文件名称。
	   如果是数字，则是打开第n+1号系统摄像头。

output: 输出存储的视频文件名称。
"""
def wsVideoPhase(input, local_view = True):
    
    W = 300
    H = 250
    RESOLUTION = (W*2, H*2)

    vid = cv2.VideoCapture(input[0])

    if not vid.isOpened():
        raise IOError("Couldn't open webcam or video: {}".format(input))

    video_FourCC    = int(vid.get(cv2.CAP_PROP_FOURCC))
    video_fps       = vid.get(cv2.CAP_PROP_FPS)
    video_size      = (int(vid.get(cv2.CAP_PROP_FRAME_WIDTH)),
                        int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    # 为normalizeCenter准备数据数组。
    center_array = []

    if local_view:
        #cv2.namedWindow("result", cv2.WINDOW_NORMAL)
        cv2.namedWindow("result")
        cv2.resizeWindow("result", 800, 400)
        #cv2.moveWindow("result", 100, 100)

    while True:
        return_value, frame = vid.read()
        
        # 根据图像特殊处理
        # ===========================
        #frame = imgRotate(frame, -10)
        (h, w) = frame.shape[:2]
        frame = frame[6*h//10:7*h//10, 4*w//9:5*w//8]
        #frame = frame[2*h//7:12*h//35, 0:w]
        #frame = frame[2*h//7:12*h//35, 123*w//280:177*w//280]
        # ===========================

        frame = cv2.resize(frame, RESOLUTION, interpolation = cv2.INTER_LINEAR)

        if type(frame) != type(None):
            
            # 根据摄像头摆放位置确定是否需要旋转图像。
            # 目前的处理逻辑是处理凸字形的焊缝折线。
            #frame = np.rot90(frame, k = 0)

            # 根据摄像头摆放位置切除多余的干扰画面。
            # 目前这个设置是基于7块样板的图像进行设置。
            # 未来这里会在GUI界面中可以设置，排除不必要的干扰区域。
            (h, w) = frame.shape[:2]
            #frame = frame[0:h, w//5:w*4//5]

            """
            if len(frame.shape) > 2:
                color_input = True
            else:
                color_input = False

            frame = cv2.resize(frame, RESOLUTION, interpolation = cv2.INTER_LINEAR)
            (h, w) = frame.shape[:2]
            """

            if local_view:
                cv2.imshow("result", frame)
                if cv2.waitKey(75) & 0xFF == ord('q'):
                    return False

        else:
            break
                
    if local_view:
        cv2.destroyAllWindows()


def main():

    parser = argparse.ArgumentParser()

    # 是否将处理后结果显示。
    parser.add_argument('-lv', '--localview', default = False, action = "store_true",
                        help = '[Optional] If shows result to local view. ')    

    # 默认处理所有文件选项。
    parser.add_argument('input', type = str, default = None, nargs = '+',
                        help = 'Input files. ')

    FLAGS = parser.parse_args()


    if FLAGS.input:
        wsVideoPhase(input = FLAGS.input,  
                     local_view = FLAGS.localview)

    else:
        print("See usage with --help.")


if __name__ == '__main__':
    main()


