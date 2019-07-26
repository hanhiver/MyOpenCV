#include <opencv2/core/core.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui/highgui.hpp>
using namespace cv;

#include <iostream>
using namespace std;

int main(int argc, char *argv[])
{
    Mat image; 

    //image = imread("./lena.jpg", 0);
    image = imread("./test.bmp", 0);

    cout<<image.rows<<endl;
    cout<<image.cols<<endl;
    
    for (int i=0; i<image.rows*image.cols; i++)
    {
        cout<<(unsigned int)image.data[i]<<" ";
    }
    cout<<endl;

    //cout<<(unsigned int)image.data[image.rows * image.cols -1]<<endl;
    
    namedWindow("DEMO", 0);

    imshow("DEMO", image);
    
    char key = (char) waitKey(0);
    
    return 0;
}

