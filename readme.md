## Prerequisites
Ubuntu 20.04
ROS noetic Desktop full


### Ros Details
Assuming that your system has ros melodic installed on your system. <strong>If not installed</strong>, please go to this [link](http://wiki.ros.org/noetic/Installation/Ubuntu), follow the instructions and install noetic full desktop version using the following commands :

	sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
    sudo apt install curl # if you haven't already installed curl
    curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -
    sudo apt update
    sudo apt install ros-noetic-desktop-full
    source /opt/ros/noetic/setup.bash

### Install ROSDEP

    sudo apt install python3-rosdep
    sudo rosdep init
    rosdep update

### Install catkin tools

    sudo sh \
    -c 'echo "deb http://packages.ros.org/ros/ubuntu `lsb_release -sc` main" \
        > /etc/apt/sources.list.d/ros-latest.list'
    
    wget http://packages.ros.org/ros.key -O - | sudo apt-key add -
    sudo apt-get update
    sudo apt-get install python3-catkin-tools

### Build Package

    cd ~/
    mkdir -p catkin_ws/src
    cd catkin_ws/src
    git clone https://github.com/jihirshu/image_stitcher.git
    cd ..
    rosdep install --from-paths src --ignore-src -r -y
    catkin build


### Run

    source devel/setup.bash
    roslaunch image_stitcher image_stitcher.launch 



