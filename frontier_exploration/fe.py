# this file is frontier exploration (this runs every time new map is generated)
import rospy
import numpy as np
from nav_msgs.msg import OccupancyGrid
from geometry_msgs.msg import Twist

class fe_run:
    def __init__(self) -> None:
        self.open_list = {"dist": [], "rad": []}
        self.move_info = {"dist": 0, "rad": 0}
        self.msg = Twist()
        self.msg.angular.x = 0.0
        self.msg.angular.y = 0.0
        self.msg.angular.z = 0.0
        self.msg.linear.x = 0.0
        self.msg.linear.y = 0.0
        self.msg.linear.z = 0.0
        self.closed_list = {"dist": np.array([]), "rad": np.array([])}
    
    def callback(self, data):
        # convert data to 2d matrix
        # data.data is a 1d array in row major order
        # first row is data.data[0:data.info.width]
        # -1 means unknown
        # 0 means free
        # 100 means occupied
        
        # clear open list
        self.open_list["dist"] = []
        self.open_list["rad"] = []
        # add 0,0 to close list
        self.closed_list["dist"] = np.append(self.closed_list["dist"], [0], axis=0)
        self.closed_list["rad"] = np.append(self.closed_list["rad"], [0], axis=0)
        
        
        # get the robots position in the occupancy grid
        cur_x = int(0 - data.info.origin.position.x / data.info.resolution)
        cur_y = int(0 - data.info.origin.position.y / data.info.resolution)
        # find all the frontiers relative to the robot
        count = 0
        for i in range(0, data.info.height):
            for j in range(0, data.info.width):
                # TODO add more checks here (cell has to border -1)
                if data.data[i*data.info.width + j] == 0:
                    count += 1
                    # find euclidean distance to robot
                    dist = ((cur_x - i)**2 + (cur_y - j)**2)**0.5
                    if dist == 0:
                        continue
                    if cur_x-i/cur_y-j < 0:
                        dist = -dist
                    if cur_y-j == 0:
                        rad = 0
                    else:
                        rad = np.arctan((cur_x - i) / (cur_y - j))
                    # check if the frontier is already in the closed list
                    if dist not in self.closed_list["dist"] and rad not in self.closed_list["rad"]:
                        self.open_list["dist"] = np.append(self.open_list["dist"], [dist], axis=0)
                        self.open_list["rad"] = np.append(self.open_list["rad"], [rad], axis=0)
        # select the farthest frontier
        max_index = np.argmax(self.open_list["dist"])
        self.move_info["dist"] = self.open_list["dist"][max_index]/data.info.width
        self.move_info["rad"] = self.open_list["rad"][max_index]
        rospy.loginfo("Moving from %s %s to %s %s %s %s", cur_x, cur_y, self.move_info["dist"], self.move_info["rad"], data.info.origin.position.x, data.info.origin.position.y)
        
        # mutate close list with the dist and rad of the frontier
        self.closed_list["dist"] = self.closed_list["dist"] - self.move_info["dist"]
        self.closed_list["rad"] = self.closed_list["rad"] - self.move_info["rad"]
    
    def run_prog(self):
        ros_pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        map_sub = rospy.Subscriber('/map', OccupancyGrid, self.callback)
        rospy.init_node('map_sub', anonymous=True)
        rate = rospy.Rate(60)
        while not rospy.is_shutdown():
            # TODO figure out moving calculations (should be trial and error)
            # there are two ways to approach this
            # 1. start with dist speed and keep decreasing speed until 0 (looks like its exploring kinda lmao)
            # 2. start with x speed and y rad and keep for s amount of time (more accurate in terms of distance)
            self.msg.linear.x = self.move_info["dist"] * 5
            self.msg.angular.z = self.move_info["rad"] / 10
            ros_pub.publish(self.msg)
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
# with ocupancy grid check for borders with 0
# add all frontiers to frontier list (priority queue)
# closest frontier is at front of the list

# select frontier closest/farthest to robot (just pop from queue) that is not in visited set
# add new frontier to the visited set

# move robot to just a certain distance away from it - cmd_vel
# move robot to frontier - publish move_base/goal to move_base
# publish to move_base/goal to move_base

# repeat