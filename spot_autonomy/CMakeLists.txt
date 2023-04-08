PROJECT(spot_autonomy)
CMAKE_MINIMUM_REQUIRED(VERSION 2.6)

SET(CMAKE_AUTOMOC ON)
SET(CMAKE_AUTORCC ON)
SET(CMAKE_AUTOUIC ON)

SET(CMAKE_CXX_FLAGS "-march=native -Wall -Werror -g -Wno-unused-function")
set(CMAKE_CXX_STANDARD 14)

IF(${CMAKE_BUILD_TYPE} MATCHES "Release")
  MESSAGE(STATUS "Additional Flags for Release mode")
  SET(CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} -fopenmp -fno-builtin-malloc \
      -fno-builtin-calloc -fno-builtin-realloc -fno-builtin-free -O3 -DNDEBUG")
  SET(BUILD_SPECIFIC_LIBRARIES "tcmalloc")
ELSEIF(${CMAKE_BUILD_TYPE} MATCHES "Debug")
  MESSAGE(STATUS "Additional Flags for Debug mode")
  SET(CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} -g")
  SET(BUILD_SPECIFIC_LIBRARIES "")
ENDIF()

MESSAGE(STATUS "SOURCE DIR: ${PROJECT_SOURCE_DIR}")

# Qt setup (needs to precede executable)
set(CMAKE_AUTOMOC on)
set(CMAKE_AUTORCC on)
set(CMAKE_AUTOUIC on)
set(CMAKE_INCLUDE_CURRENT_DIR on)
find_package(Qt5 COMPONENTS Core Widgets WebSockets REQUIRED)

FIND_PACKAGE(Lua51 REQUIRED)
FIND_PACKAGE(Eigen3 REQUIRED)
FIND_PACKAGE(Ceres REQUIRED)

INCLUDE($ENV{ROS_ROOT}/core/rosbuild/rosbuild.cmake)
ROSBUILD_INIT()
SET(ROS_BUILD_STATIC_LIBS true)
SET(ROS_BUILD_SHARED_LIBS false)

SET(EXECUTABLE_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/bin)
SET(LIBRARY_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/lib)

INCLUDE_DIRECTORIES(${PROJECT_SOURCE_DIR})

ADD_SUBDIRECTORY(amrl_shared_lib)

ROSBUILD_ADD_EXECUTABLE(enml
    enml/src/non_markov_localization_main.cpp
    enml/src/non_markov_localization.cpp
    enml/src/kdtree.cpp
    enml/src/perception_2d.cpp
    enml/src/vector_map/vector_map.cc
    enml/src/visualization/visualization.cc
    enml/src/visualization/gui_helpers.cc)
TARGET_INCLUDE_DIRECTORIES(enml PRIVATE
    amrl_shared_lib
    config_reader/include
    enml/src
    enml/src/shared
    enml/src/config-reader/include
    ${LUA_INCLUDE_DIR}
    ${CERES_INCLUDE_DIRS})
ADD_DEPENDENCIES(enml rosbuild_precompile)
TARGET_LINK_LIBRARIES(enml ceres roslib roscpp ncurses pthread boost_system
    ${LUA_LIBRARIES} rt popt glog rosbag amrl_shared_lib
    ${BUILD_SPECIFIC_LIBRARIES})

 ROSBUILD_ADD_EXECUTABLE(joystick
     joystick/joystick_driver.cc
     joystick/joystick.cc)
 TARGET_INCLUDE_DIRECTORIES(joystick PRIVATE
    config_reader/include
    amrl_shared_lib)
 TARGET_LINK_LIBRARIES(joystick gflags roslib roscpp pthread boost_system
     rt glog rosbag amrl_shared_lib ${LUA_LIBRARIES}
     ${BUILD_SPECIFIC_LIBRARIES})

ROSBUILD_ADD_EXECUTABLE(status_translator
        status_translator/status_translator.cc)
TARGET_INCLUDE_DIRECTORIES(status_translator PRIVATE
     amrl_shared_lib)
TARGET_LINK_LIBRARIES(status_translator gflags roslib
        roscpp pthread boost_system
         rt glog rosbag amrl_shared_lib
         ${BUILD_SPECIFIC_LIBRARIES})

ROSBUILD_ADD_EXECUTABLE(websocket
     webviz/src/websocket/websocket_main.cc
     webviz/src/websocket/websocket.cc)
 TARGET_INCLUDE_DIRECTORIES(websocket PRIVATE
     amrl_shared_lib
     webviz/src)
 TARGET_LINK_LIBRARIES(websocket
     Qt5::Core
     Qt5::Widgets
     Qt5::WebSockets
     glog
     gflags
     amrl_shared_lib
     ${BUILD_SPECIFIC_LIBRARIES})

ROSBUILD_ADD_EXECUTABLE(pointcloud_to_laserscan
    pointcloud_to_laserscan/pointcloud_to_laserscan_main.cc)
TARGET_INCLUDE_DIRECTORIES(pointcloud_to_laserscan PRIVATE
    config_reader/include
    amrl_shared_lib
    ${LUA_INCLUDE_DIR})
TARGET_LINK_LIBRARIES(pointcloud_to_laserscan
    glog
    gflags
    amrl_shared_lib
    roscpp
    ${LUA_LIBRARIES}
    ${BUILD_SPECIFIC_LIBRARIES})

INCLUDE_DIRECTORIES(robofleet_client/robofleet_client_lib)
INCLUDE_DIRECTORIES(robofleet_client/robofleet_client_lib/include)
ROSBUILD_ADD_EXECUTABLE(robofleet_client
    robofleet_client/src/main.cpp)
TARGET_SOURCES(robofleet_client PRIVATE
    robofleet_client/src/main.cpp
    robofleet_client/src/encode_ros.hpp
    robofleet_client/src/decode_ros.hpp
    robofleet_client/src/WsClient.hpp
    robofleet_client/src/WsServer.hpp
    robofleet_client/src/WebVizConstants.hpp
    robofleet_client/src/RosClientNode.hpp
    robofleet_client/src/MessageScheduler.hpp
)
TARGET_INCLUDE_DIRECTORIES(robofleet_client PRIVATE
    robofleet_client/src
    robofleet_client/include
    amrl_shared_lib
    config/robofleet_client
    ${LUA_INCLUDE_DIR})
TARGET_LINK_LIBRARIES(robofleet_client
    Qt5::Core
    Qt5::Widgets
    Qt5::WebSockets
    glog
    gflags
    amrl_shared_lib
    roscpp
    ${LUA_LIBRARIES}
    ${BUILD_SPECIFIC_LIBRARIES})

#  ROSBUILD_ADD_EXECUTABLE(gps_translator
#      gps/gps_translator.cc
#      visualization/visualization.cc)
#  TARGET_INCLUDE_DIRECTORIES(gps_translator PRIVATE
#      shared_lib
#      config_reader/include
#      ${LUA_INCLUDE_DIR})
#  TARGET_LINK_LIBRARIES(gps_translator gflags roslib roscpp pthread boost_system
#      rt glog rosbag amrl_shared_lib ${LUA_LIBRARIES}
#      ${BUILD_SPECIFIC_LIBRARIES})
