# npu_sim
gazebo：
建图：
roslaunch racecar_gazebo racecar.launch
roslaunch racecar_gmapping gmapping.launch
python /home/taylorbx/gazebo_sim/src/racecar_control/scripts/keyboard_teleop.py
rosrun map_server map_saver -f test
导航：
roslaunch racecar_navigation navigation.launch
