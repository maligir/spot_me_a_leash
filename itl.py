import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist

if __name__ == '__main__':
    ros_pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    rospy.init_node('spot_cmd_vel')
    rate = rospy.Rate(60)
    while not rospy.is_shutdown():
        msg = Twist()
        msg.linear.x = -0.3
        msg.linear.y = 0.0
        msg.linear.z = 0.0
        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = 0.0
        ros_pub.publish(msg)
        rate.sleep()