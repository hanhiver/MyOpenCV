#include "opencv2/opencv.hpp"
 
using namespace cv; 
using namespace std;
 
int main(int argc, char** argv)
{
    // Open video file
    VideoCapture video("video.mp4");
 
    double fps = video.get(CV_CAP_PROP_FPS);
 
    // For OpenCV 3, you can also use the following
    // double fps = video.get(CAP_PROP_FPS);
 
    cout << "Frames per second using video.get(CV_CAP_PROP_FPS) : " << fps << endl;
     
    video.release(); 
    return 0;
} 
