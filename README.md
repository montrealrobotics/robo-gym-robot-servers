# robo-gym-robot-servers

Repository containing Robot Servers ROS packages for the [robo-gym](https://github.com/jr-robotics/robo-gym) toolkit. 

The `robo-gym-robot-servers` provide an interface to the Gazebo simulations and to the real robots. 

- [Supported Systems](#supported-systems)
- [Installation](#installation)
- [How to use](#how-to-use)
- [Troubleshooting](#troubleshooting)
- [Examples](#examples)

# Supported Systems 

Recommended System Setup: Ubuntu 20.04 - ROS Noetic - Python [>3.7]

The packages are being developed for ROS Noetic.

## Robots currently implemented
- MiR100
- Universal Robots: UR3, UR3e, UR5, UR5e, UR10, UR10e, UR16
- Interbotix X-series arms: 4DOF, 5DOF and 6DOF arms
- Interbotix locobots: create3 base version

<br>

# Installation

## Ubuntu 20.04 - ROS Noetic - Python [>3.7]

1.  Setup your computer to accept software from packages.ros.org
```sh
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list' && sudo apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654
```

2. Install the required packages
```sh
sudo apt-get update && sudo apt-get install apt-utils build-essential psmisc vim-gtk git swig sudo libcppunit-dev python3-catkin-tools python3-rosdep python3-pip python3-rospkg python3-future python3-osrf-pycommon
```

3. Open a new terminal and set the environment variables. Use the same terminal for all the installation steps. 
```sh
# Set robo-gym ROS workspace folder
export ROBOGYM_WS=~/robogym_ws 
# Set ROS distribution
export ROS_DISTRO=noetic
```

4. Create a workspace folder in the home folder of your PC and clone this repository
```sh
mkdir -p $ROBOGYM_WS/src && cd $ROBOGYM_WS/src && git clone https://github.com/montrealrobotics/robo-gym-robot-servers.git
```

5. Clone required packages, build the workspace and install required python modules
For the Interbotix packages, run the standard [arm install script](https://github.com/montrealrobotics/interbotix_ros_manipulators/blob/main/interbotix_ros_xsarms/install/xsarm_remote_install.sh) or [locobot install script](https://github.com/Interbotix/interbotix_ros_rovers/blob/main/interbotix_ros_xslocobots/install/xslocobot_remote_install.sh) which will install all packages in a workspace called interbotix_ws, you can then overlay your robo-gym ws on top of this.

For the locobot workspace:

```sh
sudo apt install curl
curl 'https://raw.githubusercontent.com/Interbotix/interbotix_ros_rovers/main/interbotix_ros_xslocobots/install/xslocobot_remote_install.sh' > xslocobot_remote_install.sh
chmod +x xslocobot_remote_install.sh
./xslocobot_remote_install.sh -d noetic -b create3 -p /home/user/interbotix_rover_ws

```
Once the workspace has build, source the devel/setup.bash before building your robogym workspace to create an overlay.

If you want to use both the interbotix arms and rovers (locobots) you can also run the install script for the Interbotix arms. You can then overlay, interbotix_ws > interbotix_rover_ws > robogym_ws.
By default all robot servers are not built, to build a server, remove the CATKIN_IGNORE file in the root directory of the robot server, i.e.
```
rm ~/robo-gym-robot-servers/interbotix_rover_robot_server/CATKIN_IGNORE
```


```sh
git clone -b $ROS_DISTRO https://github.com/jr-robotics/mir_robot.git
git clone -b $ROS_DISTRO https://github.com/jr-robotics/universal_robot.git
git clone https://github.com/montrealrobotics/ur_kinematics.git
git clone -b v0.7.1-dev https://github.com/jr-robotics/franka_ros_interface
git clone https://github.com/jr-robotics/franka_panda_description
git clone -b ${ROS_DISTRO}-devel https://github.com/jr-robotics/panda_simulator
git clone https://github.com/orocos/orocos_kinematics_dynamics
cd orocos_kinematics_dynamics && git checkout b35c424e77ebc5b7e6f1c5e5c34f8a4666fbf5bc
cd $ROBOGYM_WS
sudo apt-get update
sudo rosdep init
rosdep update
rosdep install --from-paths src -i -y --rosdistro $ROS_DISTRO
catkin init
source /opt/ros/$ROS_DISTRO/setup.bash
catkin build
pip3 install robo-gym-server-modules scipy numpy
pip3 install protobuf==3.20
```

6. Add the sourcing of ROS and the ROS workspace to your `.bashrc` file:
```sh
printf "source /opt/ros/$ROS_DISTRO/setup.bash\nsource $ROBOGYM_WS/devel/setup.bash" >> ~/.bashrc
```

Source the workspace in your current terminal:

``` source $ROBOGYM_WS/devel/setup.bash ```

# Docker
To run the robo gym servers in a docker container.
Build an image with the robot type that you are working with, robot type can be **interbotix_arm**, **interbotix_rover** or **ur**:
```
sudo docker build --build-arg ROBOT_TYPE=interbotix_rover -t robot_server .
```

```
xhost +local:docker
```

Then run docker compose to start a container. You can start a container for a real robot or sim robot, by specifying the profile.
For sim:
```
sudo docker compose --profile sim up
```
For real:
```
sudo docker compose --profile real up
```
For the real robot, launch args can be passed by editing the [docker-compose.yml](docker-compose.yml). For the real interbotix_rover (locobot) the ROS_MASTER_URI can be specified here also.

# How to use

## Interbotix arms

### Simulated Robot
Simulated Robot Servers are handled by the Server Manager. If you want to manually start a Simulated Robot Server use:
```
roslaunch interbotix_arm_robot_server interbotix_arm_robot_server.launch gui:=true robot_model:=wx250s
```
Argument 'robot_model' can be any of the interbotix arm models.

### Real Robot

First, launch the robot arm control, for this, you should have previously installed the interbotix stack.
```
roslaunch interbotix_xsarm_control xsarm_control.launch robot_model:=wx250s
```
Then launch the robot server:
```
roslaunch interbotix_arm_robot_server interbotix_arm_robot_server.launch gui:=true robot_model:=wx250s real_robot:=true
```

## Interbotix rovers/locobots

### Simulated Robot
Simulated Robot Servers are handled by the Server Manager. If you want to manually start a Simulated Robot Server use:
```
roslaunch interbotix_rover_robot_server interbotix_rover_robot_server.launch gui:=true robot_model:=locobot_wx250s
```
Argument 'robot_model' can be any of the interbotix create3 base lobobot models.

### Real Robot

First, launch the locobot control on the locobot.
```
roslaunch interbotix_xslocobot_control xslocobot_control.launch use_base
```
The machine that you are running the robogym robot server on should be connected to the same network as the locobot.

Set your ROS_MASTER_URI to the locobot's IP:

```
export ROS_MASTER_URI=http://<locobot ip>:11311
```

Then launch the robot server:
```
roslaunch interbotix_rover_robot_server interbotix_rover_robot_server.launch robot_model:=locobot_wx250s real_robot:=true
```

## MiR100

### Simulated Robot
Simulated Robot Servers are handled by the Server Manager. If you want to manually start a Simulated Robot Server use:
```
roslaunch mir100_robot_server sim_robot_server.launch gui:=true
```
### Real Robot

- Connect to the robot's network

In a terminal window:
- Set ROS Master IP: `export ROS_MASTER_URI=http://192.168.12.20:11311`
- Launch MiR100 Robot Server `roslaunch mir100_robot_server real_robot_server.launch gui:=true`


## Universal Robots

### Simulated Robot
Simulated Robot Servers are handled by the Server Manager. If you want to manually start a Simulated Robot Server use:
```
roslaunch ur_robot_server ur_robot_server.launch ur_model:=ur10  gui:=true
```

### Real Robot Server
#### Install UR ROS Driver

To control the UR Robots we use the new [UR ROS Driver](https://github.com/jr-robotics/Universal_Robots_ROS_Driver).
At the current status the [UR ROS Driver](https://github.com/jr-robotics/Universal_Robots_ROS_Driver) and the [Universal_robot](https://github.com/jr-robotics/universal_robot) package use two different robot descriptions, for this reason it is needed to setup the UR ROS Driver in a separate workspace to avoid conflicts between the two packages.

```bash
# Source ROS 
source /opt/ros/$ROS_DISTRO/setup.bash

# Create a new folder for the workspace
mkdir -p ~/urdriver_ws/src
cd ~/urdriver_ws
catkin init

# Clone the necessary packages
cd ~/urdriver_ws/src
git clone https://github.com/jr-robotics/Universal_Robots_ROS_Driver.git
git clone -b calibration_devel https://github.com/fmauch/universal_robot.git

# Install dependencies
cd ~/urdriver_ws
sudo apt update -qq
rosdep update
rosdep install --from-paths src --ignore-src -y

# Build the workspace
catkin build

```

For additional instructions on how to setup the driver on the robot follow the README of the [UR ROS Driver](https://github.com/jr-robotics/Universal_Robots_ROS_Driver).

#### How to use

*NOTE:* The following instructions and command lines have been written for the UR 10 but they apply to all the supported UR robots, for instance for using the UR 5 Robot Server it is sufficient to replace `ur10` with `ur5` in all the following command lines.


- Connect to the robot's network

In a terminal window start the UR ROS driver:

```bash
# Source ROS 
source /opt/ros/$ROS_DISTRO/setup.bash

# source the UR ROS Driver workspace
source ~/urdriver_ws/devel/setup.bash

# start the Driver (replace with the IP of your robot)
roslaunch ur_robot_driver ur10_bringup.launch robot_ip:=192.168.12.70
```



In another terminal window start the Robot Server

```bash
# Source ROS 
source /opt/ros/$ROS_DISTRO/setup.bash

# source robo-gym workspace
source ~/robogym_ws/devel/setup.bash

# start the Robot Server
roslaunch ur_robot_server ur_robot_server.launch ur_model:=ur10 real_robot:=true gui:=true max_torque_scale_factor:=0.5 max_velocity_scale_factor:=0.5 speed_scaling:=0.5
```

# Troubleshooting

The Robot Server uses the standard ROS logging system, you can find the latest log of the Robot Server at: `.ros/log/latest/robot_server-*.log`

Troubleshooting problems with the robot servers can be tricky when using the server manager as launches are made in Tmux sessions. To view.
After starting the server manager with:
```
start-server-manager
```
Connect to server manager socket:
```
tmux -L ServerManager
```

You can scroll through the windows by pressing, ctrl + b followed by 'w'. When you find the window where the robot server was launched, press enter to open it.
Scrolling can be done with ctrl + b followed by '['.




# Examples

See [example_robot_server](example_robot_server) for a basic implementation of a Robot Server reduced to its minimum form. The example implements a Robot Server for the robot MiR100 with basic functionality and it is meant as a good place to start from to implement a Robot Server for your own robot. 
