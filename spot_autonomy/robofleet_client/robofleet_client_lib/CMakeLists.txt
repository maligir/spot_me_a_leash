cmake_minimum_required(VERSION 3.1.0)

PROJECT(robofleet_base_lib)

SET(CMAKE_INCLUDE_CURRENT_DIR ON)

SET(LIBS glog pthread)

SET(ROBOFLEET_LIBRARY_NAME "robofleet_base_lib"
    CACHE STRING "Name of compiled library")

SET(CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} -std=c++11")

include_directories(include)

ADD_LIBRARY(${ROBOFLEET_LIBRARY_NAME} decode.hpp encode.hpp message_structs.h MessageSchedulerLib.hpp)
TARGET_LINK_LIBRARIES(${ROBOFLEET_LIBRARY_NAME} ${LIBS}})