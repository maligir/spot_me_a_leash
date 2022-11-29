import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from sensor_msgs.msg import PointCloud2
import keyboard as kb

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)

def user_input(msg: Twist, can_get: int) -> Twist:
    if(can_get%100 == 0):
        u_input = input('Enter a direction (w, a, s, d)')
        if (u_input == ''):
            pass
        elif (u_input == 'w'):
            msg.linear.x += 0.1
            msg.angular.z = 0.0
        elif (u_input == 's'):
            msg.linear.x += -0.1
            msg.angular.z = 0.0   
        elif (u_input == 'a'):
            msg.linear.x = 0.0
            msg.angular.z += 0.1
        elif (u_input == 'd'):
            msg.linear.x = 0.0
            msg.angular.z += -0.1
 
    return msg

# def go_forward():
#     msg.linear.x = 0.3
#     msg.angular.z = 0.0

# def go_backward():
#     msg.linear.x = -0.3
#     msg.angular.z = 0.0 

# def turn_left():
#     msg.linear.x = 0.0
#     msg.angular.z = 0.3

# def turn_right():
#     msg.linear.x = 0.0
#     msg.angular.z = -0.3

def stop():
    # msg.linear.x = 0.0
    # msg.angular.z = 0.0
    pass


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
        # kb.add_hotkey('w', lambda: go_forward())
        # kb.add_hotkey('d', lambda: go_backward())
        # kb.add_hotkey('a', lambda: turn_left())
        # kb.add_hotkey('d', lambda: turn_right())
        kb.add_hotkey('enter', lambda: stop())
        # ros_pub.publish(user_input(msg, can_get))
        ros_pub.publish(msg)
        rate.sleep()

    # rospy.init_node('spot_velodyne_points', anonymous=True)
    # ros_vel = rospy.Subscriber('velodyne_points', PointCloud2, callback)
    # rate = rospy.Rate(1)
    # rospy.spin()
    # rate.sleep()