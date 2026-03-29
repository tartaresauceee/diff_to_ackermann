# Differential Drive to Ackermann Command Conversion

## Overview

The node `converter_node` implements the conversion in ROS 2. It subscribes to `/cmd_vel_diff`, where velocity commands are expressed 
in the differential drive convention, applies the conversion, and publishes the resulting commands to `/cmd_vel` in the Ackermann convention. Both topics use the standard `geometry_msgs/msg/Twist` message type.

### Dependencies
- ROS 2 Humble
- [Hunter simulation](https://github.com/agilexrobotics/ugv_gazebo_sim/tree/humble/hunter_se)

### Usage

1. Launch the Hunter simulation
``ros2 launch hunter_se_gazebo hunter_se_empty_world.launch.py``

2. Launch the converter node
``ros2 run diff_to_acker converter_node``

3. Launch rqt command gui with topic remapping
``ros2 run rqt_robot_steering rqt_robot_steering --ros-args -r /cmd_vel:=cmd_vel_diff``

## 1. Differential Drive

The differential drive robot is controlled by two inputs:
- The linear velocity $V_d$ (`linear.x`)
- The angular velocity $\omega_d$ (`angular.z`)

## 2. Ackermann

The Ackermann robot is controlled by two inputs:
- The linear velocity $V_a$ (`linear.x`)
- The steering angle $\theta_a$ (`angular.z`)

## 3. Vehicle Parameters

The following parameters are extracted from the URDF description file in `ugv_sim/hunter_se/hunter_se_description/urdf`.

|Parameter|Symbol|Value|
|---|---|---|
|Wheel base|$L$|$0.548 \text{ m}$|
|Maximum steering angle|$\theta_{max}$|$0.69 \text{ rad}$|
|Minimum turning radius|$R_{min} = L / \tan(\theta_{max})$|$0.66 \text{ m}$

## 3. Conversion

The two drive systems have different kinematics. The differential drive robot can rotate in place, while the Ackermann robot requires forward motion to turn.\
An exact mapping is therefore not possible, and the following assumptions is made:

> A pure rotation command in the differential drive system is approximated by the tightest possible curve in the Ackermann system (i.e. at maximum steering angle and minimum turning radius).

### 4.1 Linear Velocity

$$
V_a = V_d + \text{sign}(V_d) \cdot R_{min} \cdot |\omega_d| \cdot d\\
$$

where $d$ is a Gaussian centered at $V_d = 0$:

$$
d = \exp\left(-\frac{V_d^2}{V_s^2}\right)
$$

The Gaussan $d$ ensures a smooth transition between two regimes:

- **When $V_d = 0$**: $d=1$, the full rotational correction $R_{min}|\omega_d|$ is injected, achieving the tightest possible turn at the required angular velocity.
- **When $V_d \gg 0$**: $d \to 0$, the correction vanishes and $V_a \approx V_d$, recovering the standard Ackermann model.

The scaling factor $V_s$ controls the width of the Gaussian. It controls how quickly the correction fades away as linear velocity increases.

### 4.2 Steering Angle

$$
\theta_a = \text{clip}\left(\arctan\left(\frac{L \cdot \omega_d}{V_a}\right), 
-\theta_{max}, \theta_{max}\right)
$$

The result is clipped to $[-\theta_{max}, \theta_{max}]$ to respect the physical steering limits of the vehicle.

When $V_a \approx 0$, $\theta_a$ is set to 0 to avoid numerical instability.

This formula handles the pure rotation edge case such that:
- **When $V_d = 0$ and $\omega_d \neq 0$**: $\theta_a = \arctan(\frac{L}{R_{min}})$, resulting in maximum steering angle (thightest turn).