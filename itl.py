import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from sensor_msgs.msg import PointCloud2

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)

def user_input(msg: Twist) -> Twist:
    u_input = input('Enter a direction (w, a, s, d)')
    if (u_input == ''):
        pass
    elif (u_input == 'w'):
        msg.linear.x = 0.3
        msg.linear.y = 0.0
    elif (u_input == 's'):
        msg.linear.x = -0.3
        msg.linear.y = 0.0   
    elif (u_input == 'a'):
        msg.linear.x = 0.0
        msg.linear.y = -0.1
    elif (u_input == 'd'):
        msg.linear.x = 0.0
        msg.linear.y = 0.1
 
    return msg


if __name__ == '__main__':
    ros_pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    rospy.init_node('spot_cmd_vel')
    rate = rospy.Rate(60)
    msg = Twist()
    msg.angular.x = 0.0
    msg.angular.y = 0.0
    msg.angular.z = 0.0
    msg.linear.x = 0.0
    msg.linear.y = 0.0
    msg.linear.z = 0.0
    while not rospy.is_shutdown():
        ros_pub.publish(user_input())
        rate.sleep()

    # rospy.init_node('spot_velodyne_points', anonymous=True)
    # ros_vel = rospy.Subscriber('velodyne_points', PointCloud2, callback)
    # rate = rospy.Rate(1)
    # rospy.spin()
    # rate.sleep()