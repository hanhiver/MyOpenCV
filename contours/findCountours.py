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

    QUEUE_LENGTH = 40
    WINDOWS_SIZE = 20

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



# 滑动窗口比对三连张法。
def phaseVideo5(input_path, output_path = None):

    QUEUE_LENGTH = 500
    acum_frame = None
    
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
        (h, w) = frame.shape[:2]
        frame = cv2.resize(frame, (w//2, h//2), interpolation = cv2.INTER_LINEAR)
        image_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        image_to_queue = np.array(image_gray, dtype = np.uint16)
        frame_queue.append(image_to_queue)



        if acum_frame is None: 
            acum_frame = np.array(image_gray, dtype = np.uint64)
            continue

        acum_frame += image_gray

        if len(frame_queue) < QUEUE_LENGTH - 1:
            continue

        image_avg = acum_frame//QUEUE_LENGTH
        image_avg = np.array(image_avg, dtype = np.uint8)
        
        old_frame = frame_queue.pop(0)
        acum_frame -= old_frame

        blur_image = cv2.GaussianBlur(image_gray, (21, 21), 0)

        image_delta = cv2.absdiff(image_avg, blur_image)
        
        thresh = cv2.threshold(image_delta, 60, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations = 2)
        contours, hierarchy = cv2.findContours(thresh.copy(), 
                                           cv2.RETR_EXTERNAL, 
                                           cv2.CHAIN_APPROX_SIMPLE)

        contours_valid = []
        for item in contours:
            area = cv2.contourArea(item)
            if area > 1500 and area < 30000:
                contours_valid.append(item)
                print(area)

        image_contours = cv2.drawContours(image_avg//2, contours_valid, -1, (255, 255, 255), -1)

        display = np.hstack([image_gray, image_avg, image_contours])
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



# 大量照片累计干扰消除法。
def phaseVideo6(input_path, output_path = None, show_windows = False):

    acum_frame = None
    ACUM_NUMBER = 100

    acum_contours = None
    acum_contours_base = None
    
    camera = cv2.VideoCapture(input_path)
    if camera is None:
        print('Open file: {} failed. '.format(input_path))
        return

    if output_path != None:
        video_size = (1920, 756)
        video_fps = camera.get(cv2.CAP_PROP_FPS)
        video_FourCC = cv2.VideoWriter_fourcc(*'x264')
        #video_FourCC = int(camera.get(cv2.CAP_PROP_FOURCC))
        print('OUT: ', video_FourCC, video_fps, video_size)
        out = cv2.VideoWriter(output_path, video_FourCC, video_fps, video_size, False)

    frame_index = 0
    display = None

    if show_windows is True:
        cv2.namedWindow('Result', flags = cv2.WINDOW_NORMAL)

    #pre_frame = cv2.imread('mysample.jpg')
    #pre_frame = cv2.cvtColor(pre_frame, cv2.COLOR_RGB2GRAY)

    while True:
        (res, frame) = camera.read()
        if res != True:
            break

        frame_index += 1
        (h, w) = frame.shape[:2]
        #frame = frame[0:h, w//5:w*4//5]
        frame = frame[h//5:h*9//10, 0:w]
        (h, w) = frame.shape[:2]
        frame = cv2.resize(frame, (w//2, h//2), interpolation = cv2.INTER_LINEAR)
        image_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        if acum_frame is None: 
            acum_frame = np.array(image_gray, dtype = np.uint64)
            continue

        acum_frame += image_gray

        # For the first ACUM_NUMBER frames, we don't caculate the differential to avoid false alarm. 
        if frame_index < ACUM_NUMBER:
            continue

        image_avg = acum_frame//frame_index
        image_avg = np.array(image_avg, dtype = np.uint8)

        if frame_index >= 30000:
            acum_frame = acum_frame // 2
            frame_index = frame_index // 2
        
        #blur_image = cv2.GaussianBlur(image_gray, (21, 21), 0)
        blur_image = image_gray

        image_delta = cv2.absdiff(image_avg, blur_image)
        
        thresh = cv2.threshold(image_delta, 50, 255, cv2.THRESH_BINARY)[1]
        #thresh = cv2.adaptiveThreshold(image_delta, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
        thresh = cv2.dilate(thresh, None, iterations = 2)

        if cv2.__version__[0] == '3': 
            _, contours, hierarchy = cv2.findContours(thresh.copy(), 
                                           cv2.RETR_EXTERNAL, 
                                           cv2.CHAIN_APPROX_SIMPLE)
        else:
            contours, hierarchy = cv2.findContours(thresh.copy(), 
                                           cv2.RETR_EXTERNAL, 
                                           cv2.CHAIN_APPROX_SIMPLE)

        contours_valid = []
        for item in contours:
            area = cv2.contourArea(item)
            if area > 300 and area < 50000:
                contours_valid.append(item)
                #print(contours_valid)
                #print(area)

        if acum_contours is None: 
            acum_contours = np.zeros(shape = image_gray.shape, dtype = np.int16)

        frame_contours = cv2.drawContours(np.zeros(shape = image_gray.shape, dtype = np.int8), 
                                          contours_valid, -1, 2, -1)
        acum_contours += frame_contours
        acum_contours -= 1
        _, acum_contours = cv2.threshold(acum_contours, 0, 65535, cv2.THRESH_TOZERO)

        #print('Frame: ', frame_index, ' Areas: ', len(contours_valid))
        image_contours = cv2.drawContours(image_gray//2, contours_valid, -1, 255, -1)

        image_acum = acum_contours.copy()
        image_acum = cv2.threshold(image_acum, 248, 248, cv2.THRESH_TRUNC)
        image_acum = np.array(acum_contours, dtype = np.uint8)
        print('MAX:', acum_contours.max(), ' - show - ', image_acum.max())
        

        image1 = np.hstack([image_gray, image_avg])
        #image2 = np.hstack([thresh, image_contours])
        image2 = np.hstack([image_acum, image_contours])
        display = np.vstack([image1, image2])
        #display = cv2.cvtColor(display, cv2.COLOR_GRAY2RGB)
        #print('SIZE: ', display.shape)
        #display = np.hstack([image_gray, image_avg, thresh])
        #display = np.hstack([image_gray, image_contours])
        #display = frame
        
        # Already set the sample image in the begining. 
        #pre_frame = image_curr

        if output_path != None:
            out.write(display)

        if show_windows is True:
            cv2.imshow('Result', display)
            key = cv2.waitKey(1)
            if key & 0xFF == ord('q'):
                return
            elif key & 0xFF == ord('s'):
                #sample_file = input_path.split('.')[0] + '_sample.jpg'
                sample_file = 'sample.bmp'
                cv2.imwrite(sample_file, frame)


# 大量照片累计干扰消除法,合并到函数库中解决方案。
def phaseVideo7(input_path, output_path = None, show_windows = False):
    import fmfinding

    ACUM_NUMBER = 101

    fmf = fmfinding.FMFinding(width = 1920//2, height = (1080 - 1080//5 - 1080//10)//2)

    camera = cv2.VideoCapture(input_path)
    if camera is None:
        print('Open file: {} failed. '.format(input_path))
        return

    if output_path != None:
        video_size = (1920, 756)
        video_fps = camera.get(cv2.CAP_PROP_FPS)
        video_FourCC = cv2.VideoWriter_fourcc(*'x264')
        #video_FourCC = int(camera.get(cv2.CAP_PROP_FOURCC))
        print('OUT: ', video_FourCC, video_fps, video_size)
        out = cv2.VideoWriter(output_path, video_FourCC, video_fps, video_size, False)

    display = None

    if show_windows is True:
        cv2.namedWindow('Result', flags = cv2.WINDOW_NORMAL)

    while True:
        (res, frame) = camera.read()
        if res != True:
            break

        #frame_index += 1
        (h, w) = frame.shape[:2]
        #frame = frame[0:h, w//5:w*4//5]
        frame = frame[h//5:h*9//10, 0:w]
        (h, w) = frame.shape[:2]

        frame = cv2.resize(frame, (w//2, h//2), interpolation = cv2.INTER_LINEAR)

        fmf.add_new_frame(frame)

        # For the first ACUM_NUMBER frames, we don't caculate the differential to avoid false alarm. 
        if fmf.get_frame_index() < ACUM_NUMBER:
            continue

        c_max = fmf.phase_frame(frame)

        print('C_MAX: ', c_max)
        # image_avg = acum_frame//frame_index
        # image_avg = np.array(image_avg, dtype = np.uint8)

        # if frame_index >= 30000:
        #     acum_frame = acum_frame // 2
        #     frame_index = frame_index // 2
        
        # #blur_image = cv2.GaussianBlur(image_gray, (21, 21), 0)
        # blur_image = image_gray

        # image_delta = cv2.absdiff(image_avg, blur_image)
        
        # thresh = cv2.threshold(image_delta, 50, 255, cv2.THRESH_BINARY)[1]
        # #thresh = cv2.adaptiveThreshold(image_delta, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
        # thresh = cv2.dilate(thresh, None, iterations = 2)

        # if cv2.__version__[0] == '3': 
        #     _, contours, hierarchy = cv2.findContours(thresh.copy(), 
        #                                    cv2.RETR_EXTERNAL, 
        #                                    cv2.CHAIN_APPROX_SIMPLE)
        # else:
        #     contours, hierarchy = cv2.findContours(thresh.copy(), 
        #                                    cv2.RETR_EXTERNAL, 
        #                                    cv2.CHAIN_APPROX_SIMPLE)

        # contours_valid = []
        # for item in contours:
        #     area = cv2.contourArea(item)
        #     if area > 300 and area < 50000:
        #         contours_valid.append(item)
        #         #print(contours_valid)
        #         #print(area)

        # if acum_contours is None: 
        #     acum_contours = np.zeros(shape = image_gray.shape, dtype = np.int16)

        # frame_contours = cv2.drawContours(np.zeros(shape = image_gray.shape, dtype = np.int8), 
        #                                   contours_valid, -1, 2, -1)
        # acum_contours += frame_contours
        # acum_contours -= 1
        # _, acum_contours = cv2.threshold(acum_contours, 0, 65535, cv2.THRESH_TOZERO)

        #print('Frame: ', frame_index, ' Areas: ', len(contours_valid))
        #image_contours = cv2.drawContours(image_gray//2, contours_valid, -1, 255, -1)

        #image_acum = acum_contours.copy()
        #image_acum = cv2.threshold(image_acum, 248, 248, cv2.THRESH_TRUNC)
        #image_acum = np.array(acum_contours, dtype = np.uint8)
        #print('MAX:', acum_contours.max(), ' - show - ', image_acum.max())
        

        image1 = np.hstack([fmf.frame_gray, fmf.get_standard_frame()])
        print("IMAGE1:", image1.shape, fmf.get_standard_frame().shape)
        #image2 = np.hstack([thresh, image_contours])
        image2 = np.hstack([fmf.frame_gray, fmf.get_contours_frame()])
        print("IMAGE2:", image2.shape, fmf.get_contours_frame().shape)
        display = np.vstack([image1, image2])
        print(display.shape)
        #display = cv2.cvtColor(display, cv2.COLOR_GRAY2RGB)
        #print('SIZE: ', display.shape)
        #display = np.hstack([image_gray, image_avg, thresh])
        #display = np.hstack([image_gray, image_contours])
        #display = frame
        
        # Already set the sample image in the begining. 
        #pre_frame = image_curr

        if output_path != None:
            out.write(display)

        if show_windows is True:
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

    # 是否将处理后结果显示。
    parser.add_argument('-s', '--show', default = False, action = "store_true",
                        help = '[Optional] If shows result to local view. ')   

    parser.add_argument('-i', '--input', type = str, default = 'test.mp4', 
                        help = 'Input video. DEFAULT: test.mp4 ')

    parser.add_argument('-o', '--output', type = str, default = '', 
                        help = '[Optional] Output video. ')

    FLAGS = parser.parse_args()

   
    if 'input' in FLAGS:
        
        # detect_video(FLAGS.input,  
        phaseVideo7(input_path = FLAGS.input,  
                    output_path = FLAGS.output, 
                    show_windows = FLAGS.show)

    else:
        print("See usage with --help.")


if __name__ == '__main__':
    main()
