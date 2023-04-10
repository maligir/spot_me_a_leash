# this file is frontier exploration (this runs every time new map is generated)
import rospy
import numpy as np
from nav_msgs.msg import OccupancyGrid
from geometry_msgs.msg import Twist

class fe_run:
    def __init__(self) -> None:
        self.open_list = {"dist": [], "rad": [], "x": [], "y": []}
        self.msg = Twist()
        self.msg.angular.x = 0.0
        self.msg.angular.y = 0.0
        self.msg.angular.z = 0.0
        self.msg.linear.x = 0.0
        self.msg.linear.y = 0.0
        self.msg.linear.z = 0.0
        self.closed_list = {"dist": np.array([]), "rad": np.array([])}
        self.prev_map = None
        self.cur_map = None
        self.turn_time = 0
        self.move_time = 180
        self.pos_x = 1999
        self.pos_y = 1999
        self.pos_rad = 0
        self.move_info = {"dist": 0, "rad": 0}
    
    def callback(self, data):
        # convert data to 2d matrix
        # data.data is a 1d array in row major order
        # first row is data.data[0:data.info.width]
        # -1 means unknown
        # 0 means free
        # 100 means occupied
        
        self.prev_map = self.cur_map
        
        # clear open list
        self.open_list["dist"] = []
        self.open_list["rad"] = []
        # add 0,0 to close list
        self.closed_list["dist"] = np.append(self.closed_list["dist"], [0], axis=0)
        self.closed_list["rad"] = np.append(self.closed_list["rad"], [0], axis=0)
        
        # get the robots position in the occupancy grid
        # cur_x = int(0 - data.info.origin.position.x / data.info.resolution)
        # cur_y = int(0 - data.info.origin.position.y / data.info.resolution)
        # find all the frontiers relative to the robot
        for i in range(0, data.info.height):
            for j in range(0, data.info.width):
                # TODO add more checks here (cell has to border -1)
                if data.data[i*data.info.width + j] == 0:
                    # find euclidean distance to robot
                    dist = ((self.pos_x - j)**2 + (self.pos_y - i)**2)**0.5
                    if dist == 0:
                        continue
                    if self.pos_y-i == 0:
                        rad = 0
                    else:
                        rad = -np.arctan((j-self.pos_x) / (self.pos_y - i))
                    # check if the frontier is already in the closed list
                    if dist not in self.closed_list["dist"] and rad not in self.closed_list["rad"] and dist < 300:
                        # rospy.loginfo("new frontier %s", dist)
                        self.open_list["dist"] = np.append(self.open_list["dist"], [dist], axis=0)
                        rad = int(rad/0.523599)
                        if rad < 0:
                            rad = rad + 12
                        if self.pos_y-i < 0:
                            rad = (rad + 6) % 12
                        self.open_list["rad"] = np.append(self.open_list["rad"], [rad], axis=0)
                        self.open_list["x"] = np.append(self.open_list["x"], [j], axis=0)
                        self.open_list["y"] = np.append(self.open_list["y"], [i], axis=0)
        # select the farthest frontier
        max_index = np.argmax(self.open_list["dist"])
        self.move_info["dist"] = self.open_list["dist"][max_index]/data.info.width
        # movement is relative to spots orientation
        self.move_info["rad"] = self.open_list["rad"][max_index] - self.pos_rad
        self.pos_rad = self.open_list["rad"][max_index]
        self.pos_x = self.open_list["x"][max_index]
        self.pos_y = self.open_list["y"][max_index]
        rospy.loginfo("Moving %s %s %s %s", self.move_info["dist"], self.move_info["rad"], self.open_list["x"][max_index], self.open_list["y"][max_index])
        self.cur_map = data.data
        # mutate close list with the dist and rad of the frontier
        self.closed_list["dist"] = self.closed_list["dist"] - self.move_info["dist"]
        self.closed_list["rad"] = self.closed_list["rad"] - self.move_info["rad"]
        if self.move_info["dist"] < 7:
            self.turn_time = 60 * self.move_info["rad"]
        else:
            self.turn_time = 60 * abs(self.move_info["rad"] - 12)
    def run_prog(self):
        ros_pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        map_sub = rospy.Subscriber('/map', OccupancyGrid, self.callback)
        rospy.init_node('map_sub', anonymous=True)
        rate = rospy.Rate(60)
        while not rospy.is_shutdown():
            # there are two ways to approach this
            # 1. start with dist speed and keep decreasing speed until 0 (looks like its exploring kinda lmao)
            # 2. start with x speed and y rad and keep for s amount of time (more accurate in terms of distance)
            
            
            self.msg.linear.x = 0
            self.msg.angular.z = 0
            if self.turn_time > 0:
                if self.move_info["rad"] < 7:
                    self.msg.angular.z = 0.2
                else:
                    self.msg.angular.z = -0.2
                self.turn_time -= 1
            elif self.move_time > 0:
                self.msg.linear.x = 0.3
                self.move_time -= 1
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