import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg = get_package_share_directory('line_follower_car')
    world = os.path.join(pkg, 'worlds', 'line_world.world')
    sdf = os.path.join(pkg, 'models', 'car.sdf')

    return LaunchDescription([
        # Lancer Gazebo Sim
        ExecuteProcess(
            cmd=['gz', 'sim', '-r', world],
            output='screen'
        ),
        # Spawner du robot SDF
        Node(
            package='ros_gz_sim',
            executable='create',
            arguments=['-file', sdf, '-name', 'car', '-x', '0', '-y', '0', '-z', '0.1'],
            output='screen'
        ),
        # Bridge cmd_vel et camera
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            arguments=[
                '/model/car/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist',
                '/camera/image_raw@sensor_msgs/msg/Image@gz.msgs.Image',
            ],
            output='screen'
        ),
        # Nœud line follower
        Node(
            package='line_follower_car',
            executable='line_follower',
            output='screen'
        ),
    ])















































