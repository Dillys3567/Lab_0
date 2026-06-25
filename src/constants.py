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
 
# Brain should be defined by default
brain=Brain()
 
left_motor = Motor(Ports.PORT1)
right_motor = Motor(Ports.PORT10)
# reverse left motor so both motors move in the same direction
left_motor.set_reversed(True)
MAX_SPEED_RMP = 200 # rpm
MAX_SPEED_PERCENT = 100

MOTOR_RPM_CALIBRATOR = 1

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