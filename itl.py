import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from sensor_msgs.msg import PointCloud2

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)

def user_input(msg: Twist, can_get: int) -> Twist:
    if(can_get%600 == 0):
        u_input = input('Enter a direction (w, a, s, d)')
        if (u_input == ''):
            pass
        elif (u_input == 'w'):
            msg.linear.x = 0.3
            msg.angular.z = 0.0
        elif (u_input == 's'):
            msg.linear.x = -0.3
            msg.angular.z = 0.0   
        elif (u_input == 'a'):
            msg.linear.x = 0.0
            msg.angular.z = 0.3
        elif (u_input == 'd'):
            msg.linear.x = 0.0
            msg.angular.z = -0.3
 
    return msg


if __name__ == '__main__':
    ros_pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    rospy.init_node('spot_cmd_vel')
    rate = rospy.Rate(60)
    can_get = 0
    msg = Twist()
    msg.angular.x = 0.0
    msg.angular.y = 0.0
    msg.angular.z = 0.0
    msg.linear.x = 0.0
    msg.linear.y = 0.0
    msg.linear.z = 0.0
    while not rospy.is_shutdown():
        can_get+=1
        ros_pub.publish(user_input(msg, can_get))
        rate.sleep()

    # rospy.init_node('spot_velodyne_points', anonymous=True)
    # ros_vel = rospy.Subscriber('velodyne_points', PointCloud2, callback)
    # rate = rospy.Rate(1)
    # rospy.spin()
    # rate.sleep()