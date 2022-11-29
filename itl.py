import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from sensor_msgs.msg import PointCloud2


class itl_run:

    def __init__(self) -> None:
        self.direction = ""

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
            msg = Twist()
            msg.angular.x = 0.0
            msg.angular.y = 0.0
            msg.angular.z = 0.0
            msg.linear.x = 0.3
            msg.linear.y = 0.0
            msg.linear.z = 0.0
            ros_pub.publish(msg)
            # rospy.spin()
            rate.sleep()
if __name__ == '__main__':
    app_prog = itl_run()
    app_prog.run_prog()
        # rospy.init_node('spot_cmd_vel')

