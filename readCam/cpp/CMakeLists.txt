cmake_minimum_required(VERSION 2.8)
set(CMAKE_CXX_STANDARD 14)
project( readCam_cpp )
find_package( OpenCV REQUIRED )
add_executable( readCam_cpp readCam_cpp.cpp )
target_link_libraries( readCam_cpp ${OpenCV_LIBS} )

