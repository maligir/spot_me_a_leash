import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from sensor_msgs.msg import PointCloud2

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)

if __name__ == '__main__':
    rospy.init_node('itl_keyboard_sub', anonymous=True)
    ros_vel = rospy.Subscriber('itl_keyboard', String, callback)
    rospy.spin()

