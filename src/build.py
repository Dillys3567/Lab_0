"""
 Group: 2
 Members: Norvisi, Divine, Wundabli, Dillys
 we discovered that VEX V5 does not user modules so to fix this issue we added a
 builder called build_script.py, please upload build.py instead of main.py to vex
 
 to create a build.py from main, please follow these steps:
 1. please cd on terminal to src
 2. run 'python build_script.py' to generate the build.py file
 3. upload build.py to VEX

"""


# ==================================================
# BEGIN menu.py
# ==================================================


# ==================================================
# BEGIN constants.py
# ==================================================

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

def spin_left_motor(left_speed, unit=RPM):
        if (left_speed<0):
            left_motor.spin(REVERSE, abs(left_speed), unit)
        else:
            left_motor.spin(FORWARD, abs(left_speed), unit)

def spin_right_motor(right_speed, unit=RPM):
        if (right_speed<0):
            right_motor.spin(REVERSE, abs(right_speed), unit)
        else:
            right_motor.spin(FORWARD, abs(right_speed), unit)
# ==================================================
# END constants.py
# ==================================================

def padText(text):
    text = text[:MAXCHARS]
    padding = MAXCHARS - len(text)
 
    left = padding // 2
    right = padding - left
 
    result = " " * left + text + " " * right
    return result
 
 
def draw_menu():
    brain.screen.clear_screen()
    for row in range(NROWS):
        for col in range(NCOLS):
            x = SCREEN_X0 + col * (BUTTON_W + SPACING_W)
            y = SCREEN_Y0 + row * (BUTTON_H + SPACING_H)
 
            brain.screen.draw_rectangle(x, y, BUTTON_W, BUTTON_H)
 
            number = row * 3 + col + 1
            brain.screen.print_at(padText("Button " + str(number)), x=x+SPACING_W, y=y+CHAR_SPACING_Y + SPACING_H/2)
 
def renameButton(slotNumber, newName):
    slotIndex = slotNumber -1
    if slotIndex not in range(NROWS*NCOLS): 
       return
    row = slotIndex // NCOLS
    col = slotIndex % NCOLS
    x = SCREEN_X0 + col * (BUTTON_W + SPACING_W) + SPACING_W
    y = SCREEN_Y0 + row * (BUTTON_H + SPACING_H) + CHAR_SPACING_Y + SPACING_H/2
    brain.screen.print_at(padText(newName), x=x, y=y)
 
 
 
def get_button():
    while not brain.screen.pressing():
        wait(20, MSEC)

    x = brain.screen.x_position()
    y = brain.screen.y_position()

    while brain.screen.pressing():
        wait(20, MSEC)

    # convert to coordinates relative to menu origin
    x -= SCREEN_X0
    y -= SCREEN_Y0

    cell_w = BUTTON_W + SPACING_W
    cell_h = BUTTON_H + SPACING_H

    col = x // cell_w
    row = y // cell_h

    # outside grid
    if col < 0 or col >= NCOLS or row < 0 or row >= NROWS:
        return None

    # return none if inside a spacing region
    if x % cell_w > BUTTON_W:
        return None

    if y % cell_h > BUTTON_H:
        return None

    return row * NCOLS + col + 1



# ==================================================
# END menu.py
# ==================================================


# ==================================================
# BEGIN part1_functions.py
# ==================================================

 

#=================================lab0 part 1=====================================================
 
# move robot motors in the forward direction for a specified distance
def drive_straight(distance, speed):
    speed = clamp_speed_percent(speed)
    degrees = distance_to_degrees(distance)
    right_motor.spin_for(FORWARD, degrees, DEGREES, speed, PERCENT,wait=False)
    left_motor.spin_for(FORWARD, degrees, DEGREES, speed, PERCENT,wait=True)
    # left_motor.spin_for(FORWARD, degrees, DEGREES, 1.03*speed, PERCENT,wait=False)
    stop_motors(COAST)
 
# turn robot by some angle in either left or right direction
def turn(turn_angle, speed,direction):
    speed = clamp_speed_percent(speed)
    degrees = (2 * BASELINE * turn_angle)/DIAMETER
    #the directions are reversed because it was observed that the robot direction of rotation of the 
    #motor shaft either right or left was opposite to the direction of turn of the robot
    if direction is LEFT: #  
        stop_motor(LEFT)
        right_motor.spin_for(FORWARD, degrees, DEGREES, speed, PERCENT,wait=True)
        stop_motors()
    elif direction is RIGHT:
        stop_motor(RIGHT)
        left_motor.spin_for(FORWARD, degrees, DEGREES, speed, PERCENT,wait=True)
        stop_motors()
 
# spin robot on its center by some angle clockwise or anticlockwise
def spin(degrees, speed,direction):
    speed = clamp_speed_percent(speed)
    degrees = (BASELINE * degrees)/DIAMETER
    # the directions are reversed because it was observed that the robot direction of rotation of the 
    # motor shaft either right or left was opposite to the direction of turn of the robot
    if direction is LEFT:
        left_motor.spin_for(REVERSE, degrees, DEGREES, speed, PERCENT,wait=False)
        right_motor.spin_for(FORWARD, degrees, DEGREES, speed, PERCENT,wait=True)
        stop_motors()
    elif direction is RIGHT:
        left_motor.spin_for(FORWARD, degrees, DEGREES, speed, PERCENT,wait=False)
        right_motor.spin_for(REVERSE, degrees, DEGREES, speed, PERCENT,wait=True)
        stop_motors()
 
# make the robot draw the outline of a square
def square_move(distance, speed,direction):
    angle = 90
    drive_straight(distance,speed)
    turn(angle,speed,direction)
    drive_straight(distance,speed)
    turn(angle,speed,direction)
    drive_straight(distance,speed)
    turn(angle,speed,direction)
    drive_straight(distance,speed)
    turn(angle,speed,direction)
 
# make the robot draw the outline of a house 
def house_move(distance, speed,direction):
    drive_straight(distance,speed)
    turn(90,speed,direction)
    drive_straight(distance,speed)
    turn(30,speed,direction)
    drive_straight(distance,speed)
    turn(120,speed,direction)
    drive_straight(distance,speed)
    turn(30,speed,direction)
    drive_straight(distance,speed)
    turn(90,speed,direction)
 
# make the robot draw the outline of a pentagon
def pentagon(distance, speed,direction):
    angle = 78
    drive_straight(distance,speed)
    turn(angle,speed,direction)
    drive_straight(distance,speed)
    turn(angle,speed,direction)
    drive_straight(distance,speed)
    turn(angle,speed,direction)
    drive_straight(distance,speed)
    turn(angle,speed,direction)
    drive_straight(distance,speed)
    turn(angle,speed,direction)
 
#specific program
def programSelector(program):
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("Program running...")
    brain.screen.new_line()
    if program == 'straight_line':
        distance = 200
        speed_percent =20
        brain.screen.print("Driving straight for %d cm"%(distance))
        drive_straight(distance, speed_percent)
    elif program == 'turnL':
        turn_angle = 90
        direction = LEFT
        brain.screen.print("Turning %d degrees"%(turn_angle))
        turn(turn_angle,20,direction)
    elif program == 'turnR':
        turn_angle = 90
        direction = RIGHT
        brain.screen.print("Turning %d degrees"%(turn_angle))
        turn(turn_angle,20,direction)
    elif program == 'spinL':
        turn_angle = 180
        direction = LEFT
        brain.screen.print("Spin %d degrees Left"%(turn_angle))
        spin(turn_angle,20,direction)
        wait(5, SECONDS)

    elif program == 'spinR':
        turn_angle = 180
        direction = RIGHT
        brain.screen.print("Spin %d degrees Right"%(turn_angle))
        spin(turn_angle,20,direction)
        wait(5, SECONDS)
    
    elif program == 'square':
        direction = LEFT
        brain.screen.print("Draw square")
        square_move(90, 20, direction)
    elif program == 'house':
        direction = LEFT
        brain.screen.print("Draw house")
        house_move(90, 20, direction)
        brain.screen.new_line()
    elif program == 'pentagon':
        direction = LEFT
        brain.screen.print("Draw pentagon")
        pentagon(90, 20, direction)
    else:
        NOPROGRAM()
 
    brain.screen.new_line()
    brain.screen.print("Finished!")
    brain.screen.new_line()







# ==================================================
# END part1_functions.py
# ==================================================


# ==================================================
# BEGIN part2_functions.py
# ==================================================

#=================================lab0 part 2.a=====================================================
def testing_drive_values(velocity):
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("Drive straight for 200cm at %d%% speed"%(velocity))
    brain.screen.new_line()
    drive_straight(200, velocity)
   

#=================================lab0 part 2.b=====================================================
def testing_spin(velocity):
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("Spin for 360 degrees at %d%% speed"%(velocity))
    brain.screen.new_line()
    spin(360, velocity, RIGHT)

#=================================lab0 part 2.c=====================================================
def move_in_s_shape():
    brain.timer.reset()
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("moving in s shape..")
    brain.screen.new_line()
    R = 50
    theta = 270 - THETA_CORRECTION #
    arc_time = 7.5 # s
    arc_length = (2 * math.pi * R * theta)/360
    v = arc_length/arc_time
    w = v/R
    vl = v - (w * BASELINE/2)
    vr = v + (w * BASELINE/2)
    wl = 2*vl/DIAMETER
    wr = 2*vr/DIAMETER
    left_speed = clamp_speed_RPM(wl * 60/(2 * math.pi))
    right_speed = clamp_speed_RPM(wr * 60/(2 * math.pi))

    start_time = brain.timer.time(SECONDS)
    left_motor.spin(FORWARD, right_speed, RPM)
    right_motor.spin(FORWARD, left_speed, RPM)
    

    wait(arc_time, SECONDS)

    left_motor.spin(FORWARD, left_speed, RPM)
    right_motor.spin(FORWARD, right_speed, RPM)


    wait(arc_time, SECONDS)

    left_motor.stop(BRAKE)
    right_motor.stop(BRAKE)
    stop_time = brain.timer.time(SECONDS)
    run_time = stop_time - start_time
    brain.screen.print("run time =  %.2f"%(run_time))
    brain.screen.new_line()
    brain.screen.print("s shape end")
    brain.screen.new_line()
    wait(10, SECONDS)

#=================================lab0 part 2.d=====================================================
def move_in_s_shape_with_tracking():
    brain.timer.reset()
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("moving in s shape while tracking position..")
    brain.screen.new_line()
    R = 50 # cm
    theta_arc = 270
    arc_time = 7.5 # s
    arc_length = (2 * math.pi * R * theta_arc)/360
    v = arc_length/arc_time
    w = v/R
    vl = v - (w * BASELINE/2)
    vr = v + (w * BASELINE/2)
    wl = abs(2*vl/DIAMETER)
    wr = abs(2*vr/DIAMETER)
    left_speed = clamp_speed_RPM(wl * 60/(2 * math.pi))
    right_speed = clamp_speed_RPM(wr * 60/(2 * math.pi))

    x = 100 # x start
    y = 150 # y start
    theta = math.pi/2

    dt = 0.001

    brain.screen.print("x_init: %.2f, y_init: %.2f, theta_init: %.2f"%(x, y, theta*180/math.pi))
    brain.screen.new_line()

    start_time = brain.timer.time(SECONDS)

    while brain.timer.time(SECONDS) - start_time < 2 * arc_time:
        elapsed = brain.timer.time(SECONDS) - start_time

        if elapsed < arc_time-TIME_CORRECTION:
            w_arc = w
            left_motor_speed = right_speed
            right_motor_speed = left_speed
        else:
            w_arc = -w
            right_motor_speed = right_speed # wunda
            left_motor_speed = left_speed

        left_motor.spin(FORWARD, left_motor_speed, RPM)
        right_motor.spin(FORWARD, right_motor_speed, RPM)

        x += v * math.cos(theta) * dt
        y += v * math.sin(theta) * dt
        theta += w_arc * dt

        wait(dt, SECONDS)

    left_motor.stop(BRAKE)
    right_motor.stop(BRAKE)
    stop_time = brain.timer.time(SECONDS)
    run_time = stop_time - start_time
    brain.screen.print("x_end: %.2f, y_end: %.2f, theta_end: %.2f"%(x, y, theta*180/math.pi))
    brain.screen.new_line()
    brain.screen.print("run time =  %.2f"%(run_time))
    brain.screen.new_line()
    brain.screen.print("s shape 2 end")
    wait(20, SECONDS)
# ==================================================
# END part2_functions.py
# ==================================================


# ==================================================
# BEGIN part3_functions.py
# ==================================================


# ==================================================
# BEGIN sensors.py
# ==================================================


def is_object_close(distance=DISTANCE_THRESHOLD):
    if distance_sensor.object_distance(MM) < distance*10:
        return True
    return False

def configure_optical_sensor():
    optical_sensor.set_light(LedStateType.OFF)
    # optical_sensor.set_light_power(100, PERCENT)


def sense_colour():
    hue = optical_sensor.hue()
    if hue > 31 and hue < 35:
        return "yellow"
    elif hue > 80 and hue < 150:
        return "green"
    elif hue > 0 and hue < 15:
        return "red"
    elif hue > 345 and hue <= 359:
        return "red"
    elif hue > 185 and hue < 220:
        return "blue"
    else:
        return None


# ==================================================
# END sensors.py
# ==================================================



def move_in_s_shape_with_tracking_object_detection():
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("moving in s shape while detecting objects..")
    brain.screen.new_line()
    R = 50 # cm
    theta_arc = 270
    arc_time = 7.5 # s
    arc_length = (2 * math.pi * R * theta_arc)/360
    v = arc_length/arc_time
    w = v/R
    vl = v - (w * BASELINE/2)
    vr = v + (w * BASELINE/2)
    wl = abs(2*vl/DIAMETER)
    wr = abs(2*vr/DIAMETER)
    left_speed = clamp_speed_RPM(wl * 60/(2 * math.pi))
    right_speed = clamp_speed_RPM(wr * 60/(2 * math.pi))

    x = 100 # x start
    y = 150 # y start
    theta = math.pi/2

    dt = 0.008

    brain.screen.print("x_init: %.2f, y_init: %.2f, theta_init: %.2f"%(x, y, theta*180/math.pi))
    brain.screen.new_line()

    total_arc_time = 2 * arc_time
    total_time = total_arc_time + 0.6
    object_detected = False

    t=0
    start_time = brain.timer.time(SECONDS)
    while t <= total_time:
        object_detected = is_object_close()
        
        if object_detected:
            stop_motors()
            while is_object_close():
                pass

        if t < arc_time:
            w_arc = w
            left_motor_speed = left_speed
            right_motor_speed = right_speed
        else:
            w_arc = -w
            left_motor_speed = right_speed
            right_motor_speed = left_speed

        left_motor.spin(FORWARD, left_motor_speed, RPM)
        right_motor.spin(FORWARD, right_motor_speed, RPM)

        # if total_time<= total_arc_time:
        x += v * math.cos(theta) * dt
        y += v * math.sin(theta) * dt
        theta += w_arc * dt

        wait(dt, SECONDS)
        t += dt

    left_motor.stop(COAST)
    right_motor.stop(COAST)
    stop_time = brain.timer.time(SECONDS)
    run_time = stop_time - start_time 
    # brain.screen.print("x_end: %.2f, y_end: %.2f, theta_end: %.2f"%(x, y, theta*180/math.pi))
    brain.screen.new_line()
    brain.screen.print("run time =  %.2f"%(run_time))
    brain.screen.new_line()
    brain.screen.print("s shape 2 end")
    wait(20, SECONDS)

def spin_wheels(speed_percent):
    left_motor.spin(FORWARD, clamp_speed_percent(speed_percent), PERCENT)
    right_motor.spin(FORWARD, clamp_speed_percent(speed_percent), PERCENT)

def L_path_with_distance_and_colour_sensor():
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("Running L path while detecting objects and colour..")
    brain.screen.new_line()
    configure_optical_sensor()
    speed_percent = 20
    
    # 25-10 floor
    brain.screen.print("waiting..")
    brain.screen.new_line()
    print("waiting....")
    while not is_object_close(2):
        pass
    brain.screen.print("started")
    spin_wheels(speed_percent)
    while True:
        spin_wheels(speed_percent)
        colour = sense_colour()
        if colour=="blue":
            speed_percent = 35
        elif colour == "yellow":
            speed_percent = 20
            wait(0.7, SECONDS)
            stop_motors()
            turn(100, 20,RIGHT)
            speed_percent = 20
        elif colour == "red":
            stop_motors()
            while(1):
                pass

            



# ==================================================
# END part3_functions.py
# ==================================================


# ==================================================
# BEGIN part4_functions.py
# ==================================================



def move_trajectory():
    d_tiles = 100/3  #cm
    distance_unit = d_tiles * 1.5
    d_error_init = math.sqrt(2)* distance_unit
    theta_error_init = math.pi/4
    
    # Control gains
    # We will use p-control to set the linear &
    # angular velocities of the robot proportional to the errors
    # in positions and angles respectively
    w_ave= 1.85 #rad/s
    v_ave = 26.21#cm/s
    k_v_init = v_ave / d_error_init # 0.37
    k_w_init = w_ave / theta_error_init # 2.355

    k_v = 0.5
    k_omega = 2.38

    # Time parameters
    dt = 0.01  # Time step
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


        # Normalize angle error to be within -pi to pi
        angle_error = (angle_error + math.pi) % (2 * math.pi) - math.pi
        # print("theta: ",theta,  "angle error: ", angle_error * 180/math.pi, "distance: ", distance)
        
        # Compute linear and angular velocities
        # basically using p control for velocity control
        # -- we are making the target velocity proportional to the error
        v = k_v * distance
        w = k_omega * angle_error

    
    
        vl = v - (w * BASELINE/2)
        vr = v + (w * BASELINE/2)
        wl = 2*vl/DIAMETER
        wr = 2*vr/DIAMETER


        left_speed = clamp_speed_RPM(wl * 60/(2 * math.pi),100)
        right_speed = clamp_speed_RPM(wr * 60/(2 * math.pi),100)

        spin_right_motor(right_speed)
        spin_left_motor(left_speed)


        # Update robot's position and orientation
        x += v * math.cos(theta) * dt
        y += v * math.sin(theta) * dt
        theta += w * dt
        t = t+dt
        wait(dt, SECONDS)
        

    stop_motors(BRAKE)
    brain.screen.print("end of trajectory")
    brain.screen.new_line()
    wait(5, SECONDS)


def custom_move_trajectory():
    d_tiles = 100/3  #cm
    distance_unit = d_tiles * 1.5
    d_error_init = math.sqrt(2)* distance_unit
    theta_error_init = math.pi/4
    
    # Control gains
    # We will use p-control to set the linear &
    # angular velocities of the robot proportional to the errors
    # in positions and angles respectively
    w_ave= 1.85 #rad/s
    v_ave = 26.21#cm/s
    k_v_init = v_ave / d_error_init
    k_w_init = w_ave / theta_error_init

    k_v = k_v_init
    k_omega = k_w_init

    # Time parameters
    dt = 0.007  # Time step
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
        [3, 0],
        [3, 1]
    ]
    
    waypoints = [[x*distance_unit for x in row] for row in waypoints]

    next_wp_ind = 0

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

    

        # Normalize angle error to be within -pi to pi
        angle_error = (angle_error + math.pi) % (2 * math.pi) - math.pi
        # print("theta: ",theta,  "angle error: ", angle_error * 180/math.pi, "distance: ", distance)
        
        # Compute linear and angular velocities
        # basically using p control for velocity control
        # -- we are making the target velocity proportional to the error
        v = k_v * distance
        w = k_omega * angle_error

    
    
        vl = v - (w * BASELINE/2)
        vr = v + (w * BASELINE/2)
        wl = 2*vl/DIAMETER
        wr = 2*vr/DIAMETER


        # TO DO
        # limit the wheel velocities to "allowable" values based on
        # robot constraints and control the wheels.
        left_speed = clamp_speed_RPM(wl * 60/(2 * math.pi),100) # rpm
        right_speed = clamp_speed_RPM(wr * 60/(2 * math.pi),100) # rpm

        spin_right_motor(right_speed)
        spin_left_motor(left_motor)
        # Update robot's position and orientation
        x += v * math.cos(theta) * dt
        y += v * math.sin(theta) * dt
        theta += w * dt
        t = t+dt
        wait(dt, SECONDS)

    stop_motors(BRAKE)
    brain.screen.print("end of trajectory")
    brain.screen.new_line()
    wait(5, SECONDS)
# ==================================================
# END part4_functions.py
# ==================================================


# ==================================================
# BEGIN part5_functions.py
# ==================================================


# ==================================================
# BEGIN astar.py
# ==================================================

# 29th June 2026.  Ayorkor Korsah
# Code generated with the assistance of ChatGPT
# A simple implementation of A* with Euclidean costs

# ==================================================
# BEGIN heapq_vex.py
# ==================================================

# Simple binary min-heap for VEX V5 (subset of heapq)

def heappush(heap, item):
    """
    Push item into heap.
    heap: list
    item: comparable tuple like (f_score, node)
    """
    heap.append(item)
    _heapvex_sift_up(heap, len(heap) - 1)


def heappop(heap):
    """
    Pop smallest item from heap.
    """
    if not heap:
        return []

    _heapvex_swap(heap, 0, len(heap) - 1)
    item = heap.pop()

    if heap:
        _heapvex_sift_down(heap, 0)

    return item


# ------------------------------------------------------
# Internal helpers
# ------------------------------------------------------

def _heapvex_sift_up(heap, i):
    while i > 0:
        parent = (i - 1) // 2

        if heap[i][0] < heap[parent][0]:
            _heapvex_swap(heap, i, parent)
            i = parent
        else:
            break


def _heapvex_sift_down(heap, i):
    n = len(heap)

    while True:
        left = 2 * i + 1
        right = 2 * i + 2
        smallest = i

        if left < n and heap[left][0] < heap[smallest][0]:
            smallest = left

        if right < n and heap[right][0] < heap[smallest][0]:
            smallest = right

        if smallest != i:
            _heapvex_swap(heap, i, smallest)
            i = smallest
        else:
            break


def _heapvex_swap(heap, i, j):
    tmp = heap[i]
    heap[i] = heap[j]
    heap[j] = tmp
# ==================================================
# END heapq_vex.py
# ==================================================

import math

# ------------------------------------------------------
# A* WITH EUCLIDEAN COSTS
# ------------------------------------------------------

# 8-connected movement
DIRECTIONS = [
    (-1, 0),   # up
    (1, 0),    # down
    (0, -1),   # left
    (0, 1),    # right
    (-1, -1),  # up-left
    (-1, 1),   # up-right
    (1, -1),   # down-left
    (1, 1)     # down-right
]


def euclidean(a, b):
    return math.sqrt(
        (a[0] - b[0])**2 +
        (a[1] - b[1])**2
    )


def reconstruct_path(came_from, current):

    path = [current]

    while current in came_from:
        current = came_from[current]
        path.append(current)

    path.reverse()
    return path


def astar(grid, start, goal):

    rows = len(grid)
    cols = len(grid[0])

    open_set = []

    heappush(open_set, (0, start))

    came_from = {}

    g_score = {start: 0.0}

    open_hash = {start}



    while open_set:

        result = heappop(open_set)
        if result == []:
            break

        f, current = result

        if current not in open_hash:
            continue

        open_hash.remove(current)

        if current == goal:
            return reconstruct_path(came_from, current)

        for dr, dc in DIRECTIONS:

            neighbor = (current[0] + dr, current[1] + dc)
            r, c = neighbor

            if not (0 <= r < rows and 0 <= c < cols):
                continue

            if grid[r][c] == 1:
                continue

            movement_cost = euclidean(current, neighbor)

            tentative_g = g_score[current] + movement_cost

            if neighbor not in g_score or tentative_g < g_score[neighbor]:

                came_from[neighbor] = current
                g_score[neighbor] = tentative_g

                f_score = tentative_g + euclidean(neighbor, goal)

                heappush(open_set, (f_score, neighbor))
                open_hash.add(neighbor)
    return []

    
# ==================================================
# END astar.py
# ==================================================



grid = [
#    0  1  2  3  4  5
    [0, 0, 1, 0, 0, 0],  # 0
    [1, 0, 1, 1, 1, 0],  # 1
    [0, 0, 1, 0, 1, 0],  # 2
    [1, 0, 0, 0, 1, 0],  # 3
    [0, 1, 1, 1, 0, 0],  # 4
    [0, 0, 0, 0, 0, 0],  # 5
]

start = (0, 0)
goal = (5, 5)

path = astar(grid, start, goal)
print(path)


# grid = [
#     [0,0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,1,0,1,1,1,0],
#     [0,1,1,1,1,0,0,0,1,0],
#     [0,0,1,0,1,0,0,0,1,0],
#     [0,0,1,0,1,0,1,0,1,0],
#     [0,0,1,1,1,1,1,1,1,0],
#     [0,0,0,0,0,0,0,0,0,0],
# ]

# start = (0, 0)
# goal = (6, 9)

# path = astar(grid, start, goal)

# print("Path found:")
# print(path)
    



def path_planning():
    d_tiles = 100/3  #cm
    distance_unit = d_tiles
    d_error_init = math.sqrt(2)* distance_unit
    theta_error_init = math.pi/4
    
    # Control gains
    # We will use p-control to set the linear &
    # angular velocities of the robot proportional to the errors
    # in positions and angles respectively
    w_ave= 1.85 #rad/s
    v_ave = 26.21#cm/s
    k_v_init = v_ave / d_error_init
    k_w_init = w_ave / theta_error_init

    k_v = 0.5
    k_omega = 2.38

    # Time parameters
    dt = 0.01  # Time step
    total_time = 1000  # Total simulation time
    close_enough = 0.5 # How close is close enough to a waypoint?

    # Initial robot state (position and orientation)
    x = 0.0
    y = 0.0
    theta = 0.0

    # Define the trajectory (waypoints)

    
    waypoints = [[(x+0.5)*distance_unit for x in row] for row in path]

    next_wp_ind = 0

    # Simulate the robot following the trajectory
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    print("Path Planning...")
    brain.screen.print("Path planning...")
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

    

        # Normalize angle error to be within -pi to pi
        angle_error = (angle_error + math.pi) % (2 * math.pi) - math.pi
        # print("theta: ",theta,  "angle error: ", angle_error * 180/math.pi, "distance: ", distance)
        
        # Compute linear and angular velocities
        # basically using p control for velocity control
        # -- we are making the target velocity proportional to the error
        v = k_v * distance
        w = k_omega * angle_error

    
    
        vl = v - (w * BASELINE/2)
        vr = v + (w * BASELINE/2)
        wl = 2*vl/DIAMETER
        wr = 2*vr/DIAMETER


        # TO DO
        # limit the wheel velocities to "allowable" values based on
        # robot constraints and control the wheels.
        left_speed = clamp_speed_RPM(wl * 60/(2 * math.pi),100)
        right_speed = clamp_speed_RPM(wr * 60/(2 * math.pi),100)

        spin_right_motor(right_speed)
        spin_left_motor(left_speed)


        # Update robot's position and orientation
        x += v * math.cos(theta) * dt
        y += v * math.sin(theta) * dt
        theta += w * dt
        t = t+dt
        wait(dt, SECONDS)

    stop_motors(COAST)
    brain.screen.print("end of trajectory")
    brain.screen.new_line()
    wait(5, SECONDS)


# def update_grid_with_obstacle(grid, ox, oy, robot_radius, cell_size):
#     inflate = math.ceil(robot_radius / cell_size)

#     r, c = world_to_grid(ox, oy)

#     for i in range(-inflate, inflate + 1):
#         for j in range(-inflate, inflate + 1):

#             if math.sqrt(i*i + j*j) <= inflate:

#                 nr = r + i
#                 nc = c + j

#                 if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
#                     grid[nr][nc] = 1
# ==================================================
# END part5_functions.py
# ==================================================



    

#=============================main====================================================
def main():
 
  while(1):

    draw_menu() # menu has 9 buttons

    # rename buttons
    renameButton(1, "200cm line")
    renameButton(2, "L path")
    renameButton(3, "Path Planning")
    renameButton(4, "Trajectory")
    renameButton(5, "Custom Trajectory")
    renameButton(6, "TurnL")
    renameButton(7, "TurnR")
    renameButton(8, "SpinL")
    renameButton(9, "spinR")
    # renameButton(6, "House Shape")
    # renameButton(7, "S path 1")
    # renameButton(8, "S path 2")
    # renameButton(9, "Object Detection")

    button = get_button()

    if button == 1:
        programSelector('straight_line')
    elif button == 2:
        L_path_with_distance_and_colour_sensor()
    elif button == 3:
        path_planning()
    elif button == 4:
        move_trajectory()
    elif button == 5:
        custom_move_trajectory()
    elif button == 6:
        # programSelector('house')
        programSelector("turnL")
    elif button == 7:
        # move_in_s_shape()
        programSelector("turnR")
    elif button == 8:
        # move_in_s_shape_with_tracking()
        programSelector("spinL")
    elif button == 9:
        # move_in_s_shape_with_tracking_object_detection()
        programSelector("spinR")
 
main()