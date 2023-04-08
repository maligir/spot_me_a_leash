# spot_autonomy

UT Spot Autonomy Stack

## Dependencies
1. [ROS](http://wiki.ros.org/ROS/Installation)
1. System dependencies
    ```
    sudo apt install qt5-default libqt5websockets5-dev libgoogle-glog-dev libgflags-dev
    ```
1. [AMRL Fork of Clearpath Spot ROS Interface](https://github.com/ut-amrl/spot_ros), forked from https://github.com/clearpathrobotics/spot_ros

## Build
1. Clone and add repo paths to `ROS_PACKAGE_PATH`
    1.  [amrl_msgs](https://github.com/ut-amrl/amrl_msgs)
    1.  spot_autonomy 
1. Run `make`
1. Add commands to do step 1. to bashrc (otherwise need to repeat this step for launching spot_autonomy in every new shell session).

## External Hardware
* See https://github.com/ut-amrl/amrl-documentation/blob/master/robots/spot.md


## Usage

1. **Initial Setup Only:** Replicate `launch/start_clearpath_spot.launch.example` to `launch/start_clearpath_spot.launch`, filling in your Spot robot username, password, and IP address.
2. [Optional, if running under docker]:
    ```
    cd /home/amrl-user/ros-docker
    docker-compose up
    ```
    Open an interactive shell to the docker instance (run any ros/spot modules here):
    ```
    docker exec -it ros-docker_app_1 bash
    ```
4. `roslaunch spot_autonomy start_all.launch`

## Joystick

![PS4 Dualshock Controller](https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/DualShock_4.jpg/271px-DualShock_4.jpg)

* Left bumper: Press and hold for manual control
* Right bumper: Press to enable autonomous mode, press any other button to go out of autonomous mode
* Left joystick + LB: Yaw control
* Right joystick + LB: Translation control
* X button + LB: Stand up
* Square button + LB: Sit down
* Triangle button + LB: Start rosbag record
* Circle button + LB: Stop rosbag record

The rosbag record command is defined in `config/joystick.lua`.
