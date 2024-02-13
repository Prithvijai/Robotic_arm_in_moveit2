from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch import LaunchDescription
from launch.actions import ExecuteProcess, DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
import os
import xacro
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    share_dir = get_package_share_directory('cycloidal_arm')

    xacro_file = os.path.join(share_dir, 'urdf', 'cycloidal_arm.xacro')
    robot_description_config = xacro.process_file(xacro_file)
    robot_urdf = robot_description_config.toxml()

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[
            {'robot_description': robot_urdf}
        ]
    )

    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher'
    )

    gazebo_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('gazebo_ros'),
                'launch',
                'gzserver.launch.py'
            ])
        ]),
        launch_arguments={
            'pause': 'true'
        }.items()
    )

    gazebo_client = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('gazebo_ros'),
                'launch',
                'gzclient.launch.py'
            ])
        ])
    )

    urdf_spawn_node = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity', 'cycloidal_arm',
            '-topic', 'robot_description'
        ],
        output='screen'
    )
    # load_joint_state_broadcaster = ExecuteProcess(
	# 									cmd=['ros2', 'control', 'load_controller', '--set-state', 'configured','joint_state_broadcaster'],
	# 									output='screen')
    
    # start_joint_state_broadcaster = ExecuteProcess(
	# 									cmd=['ros2', 'control', 'load_controller', '--set-state', 'active','joint_state_broadcaster'],
	# 									output='screen')
    
    # load_joint_trajectory_controller = ExecuteProcess( 
	#  								cmd=['ros2', 'control', 'load_controller', '--set-state', 'configured', 'joint_trajectory_controller'], 
	#  								output='screen')

    # start_joint_trajectory_controller = ExecuteProcess(
	#  								cmd=['ros2', 'control', 'load_controller', '--set-state', 'active','joint_trajectory_controller'],
	#  								output='screen')

    return LaunchDescription([
        robot_state_publisher_node,
        joint_state_publisher_node,
        gazebo_server,
        gazebo_client,
        urdf_spawn_node,
        # load_joint_trajectory_controller,
        # start_joint_trajectory_controller
        # load_joint_trajectory_controller
    ])
