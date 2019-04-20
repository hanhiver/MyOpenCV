import cv2 
import time

def 


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
        detect_video_smooth(FLAGS.input,  
                     output_path = FLAGS.output, 
                     summary_file = FLAGS.summary,
                     stream_port = FLAGS.port,
                     camera_id = FLAGS.cnumber,
                     record_path = FLAGS.recordpath,
                     model_host = FLAGS.modelhost,
                     model_port = FLAGS.modelport,
                     local_view = FLAGS.localview)

    else:
        print("See usage with --help.")


if __name__ == '__main__':
    main()
