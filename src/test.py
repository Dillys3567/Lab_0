"""
    Group: 2
    Members: Norvisi, Divine, Wundabli, Dillys
 
"""
# library imports
from vex import *
import math
# import numpy as np
# import matplotlib.pyplot as plt

 
brain = Brain()

#===================================robot==================================================


DIAMETER = 9.92 #10.1#9.93#9.93 # wheel DIAMETER in cm #10.4
BASELINE = 30.1 #29#29.4 # baseline measurement in cm 
DISTANCE_THRESHOLD = 15 # default distance threshold in cm for object detection
# Brain should be defined by default
brain=Brain()
 
left_motor = Motor(Ports.PORT1)
right_motor = Motor(Ports.PORT10)
distance_sensor = Distance(Ports.PORT3)
optical_sensor = Optical(Ports.PORT2)
# reverse left motor so both motors move in the same direction
right_motor.set_reversed(True)
MAX_SPEED_RMP = 200 # rpm
MAX_SPEED_PERCENT = 100

MOTOR_RPM_CALIBRATOR = 1
TIME_CORRECTION = -0.2
THETA_CORRECTION = 10

velocity_values = [15, 20, 25, 30, 35, 40, 45, 50] #%


#===================================menu==================================================
SCREEN_X0 = 10
SCREEN_Y0 = 10
BUTTON_W = 140
BUTTON_H = 60
SPACING_W = 20
SPACING_H = 20
NROWS = 3
NCOLS = 3
CHAR_HEIGHT = 11
CHAR_WIDTH = 11
MAXCHARS = BUTTON_W//CHAR_WIDTH - 2
CHAR_SPACING_Y = (BUTTON_H - CHAR_HEIGHT)/2





 
# convert desired distance to angles of rotations for the powered wheels
def distance_to_degrees(distance):
    circumference = DIAMETER * math.pi
    degrees = (distance * 360) / circumference 
    return degrees
 

 
# clamp the motor power at 100%  
def clamp_speed_percent(speed_percent, max_speed_percent=MAX_SPEED_PERCENT):
    if speed_percent > max_speed_percent:
        return max_speed_percent
    elif speed_percent < -max_speed_percent:
        return -max_speed_percent
    else:
        return speed_percent
    
def clamp_speed_RPM(speed, max_speed=MAX_SPEED_RMP):
    if speed > max_speed:
        return max_speed
    elif speed < -max_speed:
        return -max_speed
    else:
        return speed
 
# stop both motors
def stop_motors(stop_type=BRAKE):
    left_motor.stop(stop_type)
    right_motor.stop(stop_type)
 
# stop either right or left motor
def stop_motor(motor, stop_type=BRAKE):
    if motor == LEFT:
        left_motor.stop(stop_type)
    elif motor == RIGHT:
        right_motor.stop(stop_type)

def NOPROGRAM(slotNumber=0):
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("No Program running...")
    brain.screen.new_line()
    if slotNumber == 0:
        brain.screen.print("No program assigned to Button")
    else:
        brain.screen.print("No program assigned to Button %d"%(slotNumber))
    wait(3, SECONDS)










distance_unit = 50#cm


# Control gains
# We will use p-control to set the linear &
# angular velocities of the robot proportional to the errors
# in positions and angles respectively
k_v = 0.37
k_omega = 2.36

# Time parameters
dt = 0.006  # Time step
total_time = 1000  # Total simulation time
close_enough = 0.5 # How close is close enough to a waypoint?

# Initial robot state (position and orientation)
x = 0.0
y = 0.0
theta = 0.0

# Define the trajectory (waypoints)

waypoints = [
    [0, 0],
    [1, 1],
    [2, 0],
    [3, 1],
    [4, 0]
]
waypoints = [[x*distance_unit for x in row] for row in waypoints]

next_wp_ind = 0

# # Storage for plotting
# x_traj = [x]
# y_traj = [y]

# Simulate the robot following the trajectory


brain.screen.clear_screen()
brain.screen.set_cursor(1, 1)
print("follow trajectory...")
brain.screen.print("follow trajectory...")
brain.screen.new_line()
t = 0
while t <= total_time:

    # if we are close enough to the next waypoint on the 
    # trajectory, move to the next waypoint
    waypoint_x = waypoints[next_wp_ind][0] 
    waypoint_y = waypoints[next_wp_ind][1] 
    dist_to_waypoint = math.sqrt((waypoint_x - x)**2 + (waypoint_y - y)**2)
    if (dist_to_waypoint < close_enough):
        next_wp_ind += 1
        brain.screen.print("At waypoint x=%.2f, y=%.2f"%(x,y))
        brain.screen.new_line()

    #Break if the robot has reached the final waypoint
    if (next_wp_ind >= len(waypoints)):
        break

    nearest_waypoint = waypoints[next_wp_ind]
    
    # Compute the control inputs
    distance = math.sqrt((nearest_waypoint[0] - x)**2 + (nearest_waypoint[1] - y)**2)
    angle_to_target = math.atan2(nearest_waypoint[1] - y, nearest_waypoint[0] - x)
    angle_error = angle_to_target - theta

 
    
#    print('nearest waypoint: ',nearest_waypoint,
#           ' distance=',distance)

    # Normalize angle error to be within -pi to pi
    angle_error = (angle_error + math.pi) % (2 * math.pi) - math.pi
    print("theta: ",theta,  "angle error: ", angle_error * 180/math.pi, "distance: ", distance)
    
    # Compute linear and angular velocities
    # basically using p control for velocity control
    # -- we are making the target velocity proportional to the error
    v = k_v * distance
    w = k_omega * angle_error

    
    # TO DO
    # for a real robot, we would need to apply inverse kinematics
    # to get the wheel velocities
  
    vl = v - (w * BASELINE/2)
    vr = v + (w * BASELINE/2)
    wl = 2*vl/DIAMETER
    wr = 2*vr/DIAMETER


    # TO DO
    # limit the wheel velocities to "allowable" values based on
    # robot constraints and control the wheels.
    left_speed = clamp_speed_RPM(wl * 60/(2 * math.pi),100)
    right_speed = clamp_speed_RPM(wr * 60/(2 * math.pi),100)

    
    if (left_speed<0):
        left_motor.spin(REVERSE, abs(left_speed), RPM)
    else:
        left_motor.spin(FORWARD, abs(left_speed), RPM)
    if(right_speed<0):
        right_motor.spin(REVERSE, abs(right_speed), RPM)
    else:
        right_motor.spin(FORWARD, abs(right_speed), RPM)


    # Update robot's position and orientation
    x += v * math.cos(theta) * dt
    y += v * math.sin(theta) * dt
    theta += w * dt
    t = t+dt
    wait(dt, SECONDS)


    
    # print(f"v={v}, omega={w}, x={x}, y={y}, theta={theta}")
    # Store the trajectory
    # x_traj.append(x)
    # y_traj.append(y)
    


# TO DO: Stop the motors once we break out of the loop!
stop_motors(BRAKE)
brain.screen.print("end of trajectory")
brain.screen.new_line()
wait(5, SECONDS)