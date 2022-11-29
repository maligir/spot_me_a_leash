import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from sensor_msgs.msg import PointCloud2

global direction

def callback(data):
    direction = data.data
    rospy.loginfo("I heard %s", direction)
    
def print_dir():
    print(direction)

if __name__ == '__main__':
    ros_pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    rospy.init_node('itl_keyboard_sub', anonymous=True)
    ros_key = rospy.Subscriber('itl_keyboard', String, callback)
    rate = rospy.Rate(60)
    while not rospy.is_shutdown():
        # print(direction)
        print_dir()
        msg = Twist()
        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = 0.0
        msg.linear.x = -0.3
        msg.linear.y = 0.0
        msg.linear.z = 0.0
        ros_pub.publish(msg)
        # rospy.spin()
        rate.sleep()


    # rospy.init_node('spot_cmd_vel')

