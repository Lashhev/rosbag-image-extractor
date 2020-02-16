cmake_minimum_required(VERSION 2.8.11)
project(bagImageExtractor)
set(CMAKE_BUILD_TYPE Debug)
# set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -march=armv8-a+crc -mtune=cortex-a53 -mfpu=crypto-neon-fp-armv8 -mfloat-abi=hard -ftree-vectorize -funsafe-math-optimizations -O3 -pipe")

set(CMAKE_INCLUDE_CURRENT_DIR ON)

find_package(OpenCV REQUIRED COMPONENTS highgui)
find_package(catkin REQUIRED COMPONENTS rosbag sensor_msgs cv_bridge)


add_library(${PROJECT_NAME} SHARED src/bagImageExtractor.cpp)
target_include_directories(${PROJECT_NAME} PUBLIC include ${OpenCV_INCLUDE_DIRS} ${catkin_INCLUDE_DIRS})
target_link_libraries(${PROJECT_NAME} ${OpenCV_LIBS} ${catkin_LIBRARIES})

add_executable(Test src/main.cpp)
target_link_libraries(Test ${PROJECT_NAME})

