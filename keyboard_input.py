import rospy
from std_msgs.msg import String

if __name__ == '__main__':
    ros_pub = rospy.Publisher('itl_keyboard', String, queue_size=10)
    rospy.init_node('itl_keyboard_pub')
    rate = rospy.Rate(60)
    while not rospy.is_shutdown():
        ros_pub.publish(input('Enter a direction (w, a, s, d)'))
        rate.sleep()
