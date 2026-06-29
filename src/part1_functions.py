from constants import *
 

#=================================lab0 part 1=====================================================
 
# move robot motors in the forward direction for a specified distance
def drive_straight(distance, speed):
    speed = clamp_speed_percent(speed)
    degrees = distance_to_degrees(distance)
    left_motor.spin_for(FORWARD, degrees, DEGREES, speed, PERCENT,wait=False)
    right_motor.spin_for(FORWARD, degrees, DEGREES, speed, PERCENT,wait=True)
    stop_motors()

 
# turn robot by some angle in either left or right direction
def turn(turn_angle, speed,direction):
    speed = clamp_speed_percent(speed)
    degrees = (2 * BASELINE * turn_angle)/DIAMETER
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
        turn_angle = 90
        direction = LEFT
        brain.screen.print("Spin %d degrees Left"%(turn_angle))
        spin(turn_angle,20,direction)
    elif program == 'spinR':
        turn_angle = 90
        direction = RIGHT
        brain.screen.print("Spin %d degrees Right"%(turn_angle))
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
    else:
        NOPROGRAM()
 
    brain.screen.new_line()
    brain.screen.print("Finished!")
    brain.screen.new_line()






