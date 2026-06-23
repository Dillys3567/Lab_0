# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Authors:      Dillys                                                    #
# 	Created:      6/23/2026, 11:19:15 AM                                       #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *
import math

"""
    Group: 2
    Members: Norvisi, Divine, Wundabli, Dillys

"""

# constants
DIAMETER = 9.93 # wheel DIAMETER in cm
BASELINE = 29.4 # baseline measurement in cm 

# Brain should be defined by default
brain=Brain()
brain.screen.print("Program running...")

left_motor = Motor(Ports.PORT1)
right_motor = Motor(Ports.PORT10)

# reverse left motor so both motors move in the same direction
left_motor.set_reversed(True)

# convert desired distance to angles of rotations for the powered wheels
def distance_to_degrees(distance):
    circumference = DIAMETER * math.pi
    degrees = (distance * 360) / circumference 
    return degrees

# clamp the motor power at 20%
def clamp_speed_20(speed):
    if speed > 20:
        return 20
    elif speed < -20:
        return -20
    else:
        return speed

# clamp the motor power at 100%  
def clamp_speed(speed):
    if speed > 100:
        return 100
    elif speed < -100:
        return -100
    else:
        return speed

# stop both motors
def stop_motors():
    left_motor.stop(BRAKE)
    right_motor.stop(BRAKE)

# stop either right or left motor
def stop_motor(motor):
    if motor == LEFT:
        left_motor.stop(BRAKE)
    elif motor == RIGHT:
        right_motor.stop(BRAKE)
        
# move robot motors in the forward direction for a specified distance
def drive_straight(distance, speed):
    speed = clamp_speed_20(speed)
    degrees = distance_to_degrees(distance)
    left_motor.spin_for(FORWARD, degrees, DEGREES, speed, PERCENT,wait=False)
    right_motor.spin_for(FORWARD, degrees, DEGREES, speed, PERCENT,wait=True)
    stop_motors()

# turn robot by some angle in either left or right direction
def turn(turn_angle, speed,direction):
    speed = clamp_speed_20(speed)
    degrees = (2 * BASELINE * turn_angle)/DIAMETER
    #the directions are reversed because it was observed that the robot direction of rotation of the 
    #motor shaft either right or left was opposite to the direction of turn of the robot
    if direction is RIGHT: #  
        stop_motor(LEFT)
        right_motor.spin_for(FORWARD, degrees, DEGREES, speed, PERCENT,wait=True)
        stop_motors()
    elif direction is LEFT:
        stop_motor(RIGHT)
        left_motor.spin_for(FORWARD, degrees, DEGREES, speed, PERCENT,wait=True)
        stop_motors()

# spin robot on its center by some angle clockwise or anticlockwise
def spin(degrees, speed,direction):
    speed = clamp_speed_20(speed)
    degrees = (BASELINE * degrees)/DIAMETER
    # the directions are reversed because it was observed that the robot direction of rotation of the 
    # motor shaft either right or left was opposite to the direction of turn of the robot
    if direction is RIGHT:
        left_motor.spin_for(REVERSE, degrees, DEGREES, speed, PERCENT,wait=False)
        right_motor.spin_for(FORWARD, degrees, DEGREES, speed, PERCENT,wait=True)
        stop_motors()
    elif direction is LEFT:
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

# run specific program
brain.screen.new_line()
program = 'square'
if program == 'straight_line':
    distance = 200
    brain.screen.print("Driving straight for %d cm"%(distance))
    drive_straight(distance, 20)
elif program == 'turn':
    turn_angle = 90
    direction = LEFT
    brain.screen.print("Turning %d degrees"%(turn_angle))
    turn(turn_angle,20,direction)
elif program == 'spin':
    turn_angle = 360
    direction = LEFT
    brain.screen.print("Spin %d degrees"%(turn_angle))
    spin(turn_angle,20,direction)
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

brain.screen.new_line()
brain.screen.print("Finished\n")
