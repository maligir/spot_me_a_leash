# this file is frontier exploration (this runs every time new map is generated)
import rospy
from nav_msgs.msg import OccupancyGrid

class fe_run:
    def __init__(self) -> None:
        pass
    
    def callback(self, data):
        print(data)
        print(data.data)
        rospy.loginfo("I heard %s", data.data)
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