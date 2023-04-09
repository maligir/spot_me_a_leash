# this file is frontier exploration (this runs every time new map is generated)
import rospy
from nav_msgs.msg import OccupancyGrid

class fe_run:
    def __init__(self) -> None:
        pass
    
    def callback(self, data):
        # file1 = open("map_data.txt","w")
        # file1.write(str(data))
        # file1.write(str(data.data))
        # convert data to 2d matrix
        temp = []
        for i in range(0, data.info.height):
            temp.append(data.data[i*data.info.width:(i+1)*data.info.width])
        cur_x = int(data.info.origin.position.x / data.info.resolution)
        cur_y = int(data.info.origin.position.y / data.info.resolution)
        for i in range(0, data.info.height):
            if 0 in temp[i]:
                rospy.loginfo("I heard %s %s", "0found", i)
            if 100 in temp[i]:
                rospy.loginfo("I heard %s %s", "100 found", i)
            break
        rospy.loginfo("I heard %s %s", cur_x, cur_y)
        pass
    
    def run_prog(self):
        map_sub = rospy.Subscriber('/map', OccupancyGrid, self.callback)
        rospy.init_node('itl_keyboard_sub', anonymous=True)
        rate = rospy.Rate(60)
        while not rospy.is_shutdown():
            rate.sleep()
        pass
    
if __name__ == "__main__":
    prog = fe_run()
    prog.run_prog()



# constantly read in the map
# done using nav_msgs/OccupancyGrid (subscribe to /map)
# use rospy to accommplish above (follow tutorial)

# repeat below steps with current map as the input

# find the frontiers
# with ocupancy grid check for borders with -1
# add all frontiers to frontier list (priority queue)
# closest frontier is at front of the list

# select frontier closest/farthest to robot (just pop from queue) that is not in visited set
# add new frontier to the visited set

# move robot to just a certain distance away from it - cmd_vel
# move robot to frontier - publish move_base/goal to move_base
# publish to move_base/goal to move_base

# repeat