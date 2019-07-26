#include <opencv2/highgui/highgui.hpp>
#include <opencv2/core/core.hpp>
#include <opencv2/imgproc/imgproc.hpp>

using namespace cv;

#include <iostream>
#include <ctime>

clock_t  start, end; 

int getCamCount()
{

	int maxTested = 10;
	for (int i = 0; i < maxTested; i++)
	{
		VideoCapture temp(i);

		bool res = temp.isOpened();
		temp.release();

		if (res)
		{
			return i;
		}
	}

	return maxTested;
}

int main()
{
	start = clock();

	int camera_index = getCamCount();

	if (camera_index >= 10)
	{
		std::cerr << "Failed to locate a cam in the system. " << std::endl;
		return 0;
	}
	else
	{
		std::cout << "Camera: <" << camera_index << "> found. Open it. " << std::endl;
	}

	//VideoCapture cap("./1s.mp4");
	//VideoCapture cap(0);
	VideoCapture cap(camera_index);

	if (!cap.isOpened())
	{
		std::cerr << "Open Video Error!" << std::endl;
	}

	cap.set(CV_CAP_PROP_FRAME_WIDTH, 320);
	cap.set(CV_CAP_PROP_FRAME_HEIGHT, 240);

	Mat srcImg, grayImg;

	namedWindow("DEMO", 1);
	
	std::cout << "Initialized in " << (float)(clock() - start) * 1000.0 / CLOCKS_PER_SEC << " ms." << std::endl;
	start = clock();

	while (true)
	{
		start = clock();
		cap.read(srcImg);
		std::cout << "Got one frame in  " << (float)(clock() - start) * 1000.0 / CLOCKS_PER_SEC << " ms."  << std::endl;
		start = clock();

		imshow("DEMO", srcImg);
		std::cout << "Show one frame in " << (float)(clock() - start) * 1000.0 / CLOCKS_PER_SEC << " ms."  << std::endl;
	
		waitKey(1000);
	}

	return 0;
}
