import rospy
from std_msgs.msg import String
import tty, sys, termios

if __name__ == '__main__':
    ros_pub = rospy.Publisher('itl_keyboard', String, queue_size=10)
    rospy.init_node('itl_keyboard_pub')
    rate = rospy.Rate(60)
    filedescriptors = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin)
    x = 0
    while not rospy.is_shutdown():
        x = sys.stdin.read(1)[0]
        ros_pub.publish(x)
        rate.sleep()




