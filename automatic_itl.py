import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from sensor_msgs.msg import PointCloud2


class itl_run:

    def __init__(self) -> None:
        self.direction = ""
        self.msg = Twist()
        self.msg.angular.x = 0.0
        self.msg.angular.y = 0.0
        self.msg.angular.z = 0.0
        self.msg.linear.x = 0.0
        self.msg.linear.y = 0.0
        self.msg.linear.z = 0.0

    def callback(self, data):
        self.direction = data.data
        print(self.direction)
        rospy.loginfo("I heard %s", self.direction)

    def run_prog(self):
        ros_pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        rospy.init_node('itl_keyboard_sub', anonymous=True)
        ros_key = rospy.Subscriber('itl_keyboard', String, self.callback)
        rate = rospy.Rate(60)
        while not rospy.is_shutdown():
            print(self.direction)
            if (self.direction == ''):
                pass
            elif (self.direction == 'w'):
                self.msg.linear.x += 0.1
                self.msg.angular.z += 0.0
            elif (self.direction == 's'):
                self.msg.linear.x += -0.1
                self.msg.angular.z += 0.0   
            elif (self.direction == 'a'):
                self.msg.linear.x += 0.0
                self.msg.angular.z += 0.1
            elif (self.direction == 'd'):
                self.msg.linear.x += 0.0
                self.msg.angular.z += -0.1
            elif (self.direction == 'z'):
                self.msg.linear.x = 0.0
                self.msg.angular.z = 0.0
            
            if self.msg.linear.x > 0 and self.msg.linear.x < 0.2 and self.direction == 'w':
                self.msg.linear.x = 0.2
            elif self.msg.linear.x < 0 and self.msg.linear.x > -0.2 and self.direction == 's':
                self.msg.linear.x = -0.2
            elif self.msg.linear.x > 1.9:
                self.msg.linear.x = 1.9
            elif self.msg.linear.x < -1.9:
                self.msg.linear.x = -1.9
            self.direction = ''
            ros_pub.publish(self.msg)
            print(self.msg.angular.z)
            rate.sleep()
            # 1.9, -1.9
if __name__ == '__main__':
    app_prog = itl_run()
    app_prog.run_prog()
        # rospy.init_node('spot_cmd_vel')
