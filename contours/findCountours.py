import cv2 
import time
import argparse
import numpy as np 

# 传统方式检测高速公路异物。
def phaseVideo(input_path, output_path = None):
    camera = cv2.VideoCapture(input_path)
    if camera is None:
        print('Open file: {} failed. '.format(input_path))
        return

    pre_frame = cv2.imread('mysample.jpg')
    pre_frame = cv2.cvtColor(pre_frame, cv2.COLOR_RGB2GRAY)

    if output_path != None:
        video_size = (int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)),
                        int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        video_FourCC = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(output_path, video_FourCC, 25, video_size)

    #pre_frame = None
    display = None

    cv2.namedWindow('Result', flags = cv2.WINDOW_NORMAL)

    while True:
        (res, frame) = camera.read()
        if res != True:
            break

        image_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        image_blur = cv2.GaussianBlur(image_gray, (21, 21), 0)

        image_curr = image_gray

        if pre_frame is None:
            pre_frame = image_curr
        else:
            image_delta = cv2.absdiff(pre_frame, image_curr)
            thresh = cv2.threshold(image_delta, 80, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations = 2)
            contours, hierarchy = cv2.findContours(thresh.copy(), 
                                               cv2.RETR_EXTERNAL, 
                                               cv2.CHAIN_APPROX_SIMPLE)

            contours_valid = []
            for item in contours:
                if cv2.contourArea(item) > 300:
                    #rect = cv2.boundingRect(item)
                    #print('Contour:', item)
                    #print('Rect: ', rect)
                    contours_valid.append(item)
                    #image_delta = cv2.rectangle(image_delta, 
                    #image_delta = cv2.rectangle(frame,     
                    #                            (rect[0], rect[1]), 
                    #                            (rect[0] + rect[2], rect[1] + rect[3]), 
                    #                            (255, 255, 255), 2)

            image_contours = cv2.drawContours(image_delta, contours_valid, -1, (255, 255, 255), 1)
            #image_contours = image_delta

            #print('Size of contours: ', len(contours))
            #for item in contours:
            #    print('   ==> countour size: ', cv2.contourArea(item))

            display = np.hstack([image_curr, image_contours])
            #display = frame
            
            # Already set the sample image in the begining. 
            #pre_frame = image_curr

            if output_path != None:
                out.write(display)

            cv2.imshow('Result', display)
            key = cv2.waitKey(1)
            if key & 0xFF == ord('q'):
                return
            elif key & 0xFF == ord('s'):
                #sample_file = input_path.split('.')[0] + '_sample.jpg'
                sample_file = 'sample.bmp'
                cv2.imwrite(sample_file, frame)

# 像素流动方式检测
def phaseVideo3(input_path, output_path = None):
    camera = cv2.VideoCapture(input_path)
    if camera is None:
        print('Open file: {} failed. '.format(input_path))
        return

    if output_path != None:
        video_size = (int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)),
                        int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        video_FourCC = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(output_path, video_FourCC, 25, video_size)

    pre_frame = None
    acum_frame = None
    frame_index = 0
    display = None
    contours = []
    contours_valid = []

    cv2.namedWindow('Result', flags = cv2.WINDOW_NORMAL)

    #pre_frame = cv2.imread('mysample.jpg')
    #pre_frame = cv2.cvtColor(pre_frame, cv2.COLOR_RGB2GRAY)

    while True:
        (res, frame) = camera.read()
        if res != True:
            break

        frame_index += 1
        image_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        if acum_frame is None:
            acum_frame = np.array(image_gray, dtype = np.uint64)
            continue

        acum_frame += image_gray
        image_avg = acum_frame//frame_index
        image_avg = np.array(image_avg, dtype = np.uint8)

        if frame_index % 300 == 0:
            if pre_frame is None:
                pre_frame = image_avg
                continue


            image_delta = cv2.absdiff(image_avg, pre_frame)
            
            thresh = cv2.threshold(image_delta, 10, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations = 2)
            contours, hierarchy = cv2.findContours(thresh.copy(), 
                                               cv2.RETR_EXTERNAL, 
                                               cv2.CHAIN_APPROX_SIMPLE)

            contours_valid = []
            for item in contours:
                area = cv2.contourArea(item)
                if area > 1000 and area < 10000:
                    contours_valid.append(item)
                    print(area)

        image_contours = cv2.drawContours(image_avg//2, contours_valid, -1, (255, 255, 255), 1)

        display = np.hstack([image_gray, image_contours])
        #display = np.hstack([image_gray, image_contours])
        #display = frame
        
        # Already set the sample image in the begining. 
        #pre_frame = image_curr

        if output_path != None:
            out.write(display)

        cv2.imshow('Result', display)
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            return
        elif key & 0xFF == ord('s'):
            #sample_file = input_path.split('.')[0] + '_sample.jpg'
            sample_file = 'sample.bmp'
            cv2.imwrite(sample_file, frame)


# 像素流动方式检测
def phaseVideo4(input_path, output_path = None):
    camera = cv2.VideoCapture(input_path)
    if camera is None:
        print('Open file: {} failed. '.format(input_path))
        return

    if output_path != None:
        video_size = (int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)),
                        int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        video_FourCC = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(output_path, video_FourCC, 25, video_size)

    pre_frame = None
    acum_frame = None
    frame_index = 0
    display = None
    contours = []
    contours_valid = []

    cv2.namedWindow('Result', flags = cv2.WINDOW_NORMAL)

    #pre_frame = cv2.imread('mysample.jpg')
    #pre_frame = cv2.cvtColor(pre_frame, cv2.COLOR_RGB2GRAY)

    while True:
        (res, frame) = camera.read()
        if res != True:
            break

        frame_index += 1
        image_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        if acum_frame is None:
            acum_frame = np.array(image_gray, dtype = np.uint64)
            continue

        acum_frame += image_gray
        image_avg = acum_frame//frame_index
        image_avg = np.array(image_avg, dtype = np.uint8)

        display = np.hstack([image_gray, image_avg])
        #display = np.hstack([image_gray, image_contours])
        #display = frame
        
        # Already set the sample image in the begining. 
        #pre_frame = image_curr

        if output_path != None:
            out.write(display)

        cv2.imshow('Result', display)
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            return
        elif key & 0xFF == ord('s'):
            #sample_file = input_path.split('.')[0] + '_sample.jpg'
            sample_file = 'sample.bmp'
            cv2.imwrite(sample_file, frame)


# 滑动窗口法
def phaseVideo4(input_path, output_path = None):

    QUEUE_LENGTH = 20
    WINDOWS_SIZE = 10

    camera = cv2.VideoCapture(input_path)
    if camera is None:
        print('Open file: {} failed. '.format(input_path))
        return

    if output_path != None:
        video_size = (int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)),
                        int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        video_FourCC = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(output_path, video_FourCC, 25, video_size)

    frame_index = 0
    display = None
    frame_queue = []

    cv2.namedWindow('Result', flags = cv2.WINDOW_NORMAL)

    #pre_frame = cv2.imread('mysample.jpg')
    #pre_frame = cv2.cvtColor(pre_frame, cv2.COLOR_RGB2GRAY)

    while True:
        (res, frame) = camera.read()
        if res != True:
            break

        frame_index += 1
        image_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        image_to_queue = np.array(image_gray, dtype = np.uint16)
        frame_queue.append(image_to_queue)

        if len(frame_queue) < QUEUE_LENGTH - 1:
            continue

        pre_frame = np.sum(frame_queue[:WINDOWS_SIZE], axis = 0)
        pst_frame = np.sum(frame_queue[-WINDOWS_SIZE:], axis = 0)

        pre_frame = np.array(pre_frame//WINDOWS_SIZE, dtype = np.uint8)
        pst_frame = np.array(pst_frame//WINDOWS_SIZE, dtype = np.uint8)

        frame_queue.pop(0)

        display = np.hstack([image_gray, pre_frame, pst_frame])
        #display = np.hstack([image_gray, image_contours])
        #display = frame
        
        # Already set the sample image in the begining. 
        #pre_frame = image_curr

        if output_path != None:
            out.write(display)

        cv2.imshow('Result', display)
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            return
        elif key & 0xFF == ord('s'):
            #sample_file = input_path.split('.')[0] + '_sample.jpg'
            sample_file = 'sample.bmp'
            cv2.imwrite(sample_file, frame)

def phaseVideo2(input_path, output_path = None):
    camera = cv2.VideoCapture(input_path)
    if camera is None:
        print('Open file: {} failed. '.format(input_path))
        return

    if output_path != None:
        video_size = (int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)),
                        int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        video_FourCC = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(output_path, video_FourCC, 25, video_size)

    pre_frame = None
    display = None

    cv2.namedWindow('Result', flags = cv2.WINDOW_NORMAL)

    pre_frame = cv2.imread('mysample.jpg')
    pre_frame = cv2.cvtColor(pre_frame, cv2.COLOR_RGB2GRAY)

    while True:
        (res, frame) = camera.read()
        if res != True:
            break

        image_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        image_gray = cv2.GaussianBlur(image_gray, (21, 21), 0)
        image_curr = image_gray

        image_delta = cv2.absdiff(pre_frame, image_curr)
        thresh = cv2.threshold(image_gray, 80, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations = 2)
        contours, hierarchy = cv2.findContours(thresh.copy(), 
                                           cv2.RETR_EXTERNAL, 
                                           cv2.CHAIN_APPROX_SIMPLE)
        """
        contours_valid = []
        for item in contours:
            if cv2.contourArea(item) > 300:
                rect = cv2.boundingRect(item)
                #print('Contour:', item)
                #print('Rect: ', rect)
                contours_valid.append(rect)
                #image_delta = cv2.rectangle(image_delta, 
                #image_delta = cv2.rectangle(frame,     
                #                            (rect[0], rect[1]), 
                #                            (rect[0] + rect[2], rect[1] + rect[3]), 
                #                            (255, 255, 255), 2)
        """

        image_contours = cv2.drawContours(image_gray, contours, -1, (255, 255, 255), 1)
        #image_contours = image_delta

        #print('Size of contours: ', len(contours))
        #for item in contours:
        #    print('   ==> countour size: ', cv2.contourArea(item))

        display = np.hstack([image_gray, image_contours])
        #display = frame
        
        # Already set the sample image in the begining. 
        #pre_frame = image_curr

        if output_path != None:
            out.write(display)

        cv2.imshow('Result', display)
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            return
        elif key & 0xFF == ord('s'):
            #sample_file = input_path.split('.')[0] + '_sample.jpg'
            sample_file = 'sample.bmp'
            cv2.imwrite(sample_file, frame)



def main():

    global logger_manager
    global logger 
    global class_names
    global colors

    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input', type = str, default = 'test.mp4', 
                        help = 'Input video. DEFAULT: test.mp4 ')

    parser.add_argument('-o', '--output', type = str, default = '', 
                        help = '[Optional] Output video. ')

    FLAGS = parser.parse_args()

   
    if 'input' in FLAGS:
        
        # detect_video(FLAGS.input,  
        phaseVideo4(input_path = FLAGS.input,  
                   output_path = FLAGS.output)

    else:
        print("See usage with --help.")


if __name__ == '__main__':
    main()
