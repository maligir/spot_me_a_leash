--[[
record_cmd = "rosbag record /status /velodyne_points /scan /imu/data /jackal_velocity_controller/odom /gps/fix /gps/vel /imu/data_raw /tf /localization /move_base_simple/goal /navigation/cmd_vel /set_nav_target /set_pose"..
    " /image_raw/compressed "..
    " /joint_states"..
    " /joystick"..
    " /odom"..
    " /spot/camera/frontright/image/compressed "..
    " /spot/camera/frontleft/image/compressed "..
    " /spot/camera/right/image/compressed "..
    " /spot/camera/left/image/compressed "..
    " /spot/camera/back/image/compressed "..
    " /spot/camera/frontright/camera_info"..
    " /spot/camera/frontleft/camera_info"..
    " /spot/camera/right/camera_info"..
    " /spot/camera/left/camera_info"..
    " /spot/camera/back/camera_info __name:=joystick_rosbag_record&";
   --]]
record_cmd = "rosbag record"..
    " /odom"..
    " /velodyne_2dscan_highbeams"..
    " /scan"..
    " __name:=joystick_rosbag_record &";
