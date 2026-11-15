import os
from launch import LaunchDescription
from launch_ros.actions import Node

URDF_YOLU = os.path.expanduser('~/robotik/robot/depo_robotu.urdf')


def generate_launch_description():
    with open(URDF_YOLU) as dosya:
        robot_tarifi = dosya.read()

    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': robot_tarifi}],
        ),
        Node(
            package='ros_gz_sim',
            executable='create',
            arguments=['-topic', 'robot_description',
                       '-name', 'depo_robotu',
                       '-z', '0.3'],
        ),
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            arguments=['/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist'],
        ),
    ])