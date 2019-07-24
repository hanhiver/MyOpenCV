#include <opencv2/highgui/highgui.hpp>
#include <opencv2/core/core.hpp>
#include <opencv2/imgproc/imgproc.hpp>

using namespace cv;

#include <iostream>
#include <ctime>

clock_t  start, end; 

int main()
{
	start = clock();
	//VideoCapture cap("./1s.mp4");
	VideoCapture cap(2);

	if (!cap.isOpened())
	{
		std::cerr << "Open Video Error!" << std::endl;
	}

	Mat srcImg, grayImg;

	namedWindow("DEMO", 1);
	
	std::cout << "Initialized in " << (float)(clock() - start) * 1000.0 / CLOCKS_PER_SEC << " ms." << std::endl;
	start = clock();

	while (cap.read(srcImg))
	{
		std::cout << "Got one frame in  " << (float)(clock() - start) * 1000.0 / CLOCKS_PER_SEC << " ms."  << std::endl;
		start = clock();

		imshow("DEMO", srcImg);
		std::cout << "Show one frame in " << (float)(clock() - start) * 1000.0 / CLOCKS_PER_SEC << " ms."  << std::endl;
		
		waitKey(1);
		start = clock();
	}

	return 0;
}
