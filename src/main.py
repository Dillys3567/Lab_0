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

#===================================menu==================================================
X0 = 10
Y0 = 10
BUTTON_W = 140
BUTTON_H = 60
SPACING_W = 20
SPACING_H = 20
NROWS = 3
NCOLS = 3
CHAR_HEIGHT = 11
CHAR_WIDTH = 11
MAXCHARs = BUTTON_W//CHAR_WIDTH - 2
CHAR_SPACING_Y = (BUTTON_H - CHAR_HEIGHT)/2
 
 
def padText(text):
    text = text[:MAXCHARs]
    padding = MAXCHARs - len(text)
 
    left = padding // 2
    right = padding - left
 
    result = " " * left + text + " " * right
    return result
 
 
def draw_menu():
    brain.screen.clear_screen()
    for row in range(NROWS):
        for col in range(NCOLS):
            x = X0 + col * (BUTTON_W + SPACING_W)
            y = Y0 + row * (BUTTON_H + SPACING_H)
 
            brain.screen.draw_rectangle(x, y, BUTTON_W, BUTTON_H)
 
            number = row * 3 + col + 1
            brain.screen.print_at(padText("Slot " + str(number)), x=x+SPACING_W, y=y+CHAR_SPACING_Y + SPACING_H/2)
 
def renameSlot(slotNumber, newName):
    slotIndex = slotNumber -1
    if slotIndex not in range(NROWS*NCOLS): 
       return
    row = slotIndex // NCOLS
    col = slotIndex % NROWS
    x = X0 + col * (BUTTON_W + SPACING_W) + SPACING_W
    y = Y0 + row * (BUTTON_H + SPACING_H) + CHAR_SPACING_Y + SPACING_H/2
    brain.screen.print_at(padText(newName), x=x, y=y)
 
 
 
def get_button():
    while not brain.screen.pressing():
        wait(20, MSEC)
 
    x = brain.screen.x_position()
    y = brain.screen.y_position()
 
    while brain.screen.pressing():
        wait(20, MSEC)
 
    col = x // BUTTON_W
    row = y // BUTTON_H
 
    return row * 3 + col + 1
 
 
#=================================lab0 part 1=====================================================
 
# constants
DIAMETER = 9.93#9.93 # wheel DIAMETER in cm #10.4
BASELINE = 29.4 # baseline measurement in cm 
 
# Brain should be defined by default
brain=Brain()
 
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
def clamp_speed_RPM(speed, max_speed):
    if speed > max_speed:
        return max_speed
    elif speed < -max_speed:
        return -max_speed
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

def drive_straight_100(distance, speed):
    speed = clamp_speed(speed)
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
    speed = clamp_speed(speed)
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
 
#specific program
def programSelector(program):
    brain.screen.clear_screen()
    brain.screen.print("Program running...")
    brain.screen.new_line()
    if program == 'straight_line':
        distance = 200
        brain.screen.print("Driving straight for %d cm"%(distance))
        drive_straight(distance, 20)
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
    elif program == 'spin':
        turn_angle = 90
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
    brain.screen.print("Finished")
    brain.screen.new_line()

#=================================lab0 part 2.a=====================================================
velocity_values = [15, 20, 25, 30, 35, 40, 45, 50] #%
MAX_SPEED = 200 #rpm
def testing_drive_values(velocity):
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("Drive straight for 200cm at %d%% speed"%(velocity))
    brain.screen.new_line()
    drive_straight_100(200, velocity)
   

#=================================lab0 part 2.b=====================================================
def testing_spin(velocity):
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("Spin for 360 degrees at %d%% speed"%(velocity))
    brain.screen.new_line()
    spin(360, velocity, RIGHT)

#=================================lab0 part 2.c=====================================================
def testing_first_S():
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("s shape part 1")
    brain.screen.new_line()
    R = 50
    theta = 270
    arc_time = 7.5 # s
    arc_length = (2 * math.pi * R * theta)/360
    v = arc_length/arc_time
    w = v/R
    vl = v - (w * BASELINE/2)
    vr = v + (w * BASELINE/2)
    wl = 2*vl/DIAMETER
    wr = 2*vr/DIAMETER
    left_speed = clamp_speed_RPM(wl * 60/(2 * math.pi), MAX_SPEED)
    right_speed = clamp_speed_RPM(wr * 60/(2 * math.pi), MAX_SPEED)

    left_motor.spin(FORWARD, right_speed, RPM)
    right_motor.spin(FORWARD, left_speed, RPM)
    

    wait(arc_time, SECONDS)

    left_motor.spin(FORWARD, left_speed, RPM)
    right_motor.spin(FORWARD, right_speed, RPM)


    wait(arc_time, SECONDS)

    left_motor.stop(BRAKE)
    right_motor.stop(BRAKE)

   
    brain.screen.print("s shape end")
    brain.screen.new_line()


def testing_second_S():
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("s shape part 2")
    brain.screen.new_line()
    R = 50
    theta_arc = 270
    arc_time = 7.5 # s
    arc_length = (2 * math.pi * R * theta_arc)/360
    v = arc_length/arc_time
    w = v/R
    vl = v - (w * BASELINE/2)
    vr = v + (w * BASELINE/2)

    x = 100
    y = 150
    theta = math.pi/2
    
    dt = 0.001
    arc_time = 7.5 # seconds
 
    
    t = 0
    brain.screen.print("x initial: %.2f, y initial: %.2f"%(x, y))
    brain.screen.new_line()
    while t < 2*arc_time:
        if t < arc_time:
            # print("in first loop")
            vL_loop = vr
            vR_loop = vl
        else:
            # print("in second loop")
            vL_loop = vl
            vR_loop = vr
       
        
        w_loop = (vR_loop- vL_loop)/BASELINE
        wl = 2*vL_loop/DIAMETER
        wr = 2*vR_loop/DIAMETER
        left_speed = clamp_speed_RPM(wl * 60/(2 * math.pi), MAX_SPEED)
        right_speed = clamp_speed_RPM(wr * 60/(2 * math.pi), MAX_SPEED)
        left_motor.spin(FORWARD, left_speed*1.1, RPM)
        right_motor.spin(FORWARD, right_speed, RPM)

        x += v * math.cos(theta) * dt
        y += v * math.sin(theta) * dt
        theta += -w_loop * dt
        # print("theta: %.2f, x: %.2f, y: %.2f"%(theta * 180/math.pi, x, y))
        wait(dt, SECONDS)
        t += dt

 
    left_motor.stop(BRAKE)
    right_motor.stop(BRAKE)
    brain.screen.print("xfinal: %.2f, y final: %.2f"%(x, y))
    brain.screen.new_line()
    brain.screen.print("s shape 2 end")


    # brain.screen.clear_screen()
    # brain.screen.set_cursor(1, 1)
    # brain.screen.print("s shape part 2")
    # brain.screen.new_line()
    # R = 50
    # theta = 270
    # arc_time = 7.5 # s
    # arc_length = (2 * math.pi * R * theta)/360
    # v = arc_length/arc_time
    # w = v/R
    # vl = v - (w * BASELINE/2)
    # vr = v + (w * BASELINE/2)
    # wl = 2*vl/DIAMETER
    # wr = 2*vr/DIAMETER
    # left_speed = clamp_speed_RPM(wl * 60/(2 * math.pi), MAX_SPEED)
    # right_speed = clamp_speed_RPM(wr * 60/(2 * math.pi), MAX_SPEED)
    # dt = 0.01

    # # Initial position and orientation of the robot
    # radius_circle = R
    # x = radius_circle  # Starting on the circumference of the circle
    # y = 0.0
    # theta = math.pi / 2  # Facing upwards

    # # Storage for plotting
    # x_traj = [x]
    # y_traj = [y]

    # # Compute the angular velocity
    # omega = w
    # total_time = 2 * arc_time  # Total time for the S-trajectory

    # t = 0
    # brain.screen.print("x initial: %.2f, y initial: %.2f"%(x, y))
    # brain.screen.new_line()
    # while t <= total_time:
    #     # Switch omega direction at halfway point for S-trajectory
    #     if t < total_time / 2:
    #         omega_current = v / radius_circle  # Left curve
    #     else:
    #         omega_current = -v / radius_circle  # Right curve

    #     # Compute wheel velocities
    #     v_l = v - (BASELINE / 2) * omega_current
    #     v_r = v + (BASELINE / 2) * omega_current
    #     wl = 2*vl/DIAMETER
    #     wr = 2*vr/DIAMETER
    #     left_speed = clamp_speed_RPM(wl * 60/(2 * math.pi), MAX_SPEED)
    #     right_speed = clamp_speed_RPM(wr * 60/(2 * math.pi), MAX_SPEED)
    #     left_motor.spin(FORWARD, left_speed, RPM)
    #     right_motor.spin(FORWARD, right_speed, RPM)

    #     # Update robot's position and orientation
    #     v = (v_l + v_r) / 2
    #     theta += omega_current * dt
    #     x += v * math.cos(theta) * dt
    #     y += v * math.sin(theta) * dt

    #     # Store the trajectory
    #     x_traj.append(x)
    #     y_traj.append(y)
    #     print("t: %.2f, x: %.2f, y: %.2f"%(t, x, y))
    #     wait(dt, SECONDS)
    #     t += dt



    # left_motor.stop(BRAKE)
    # right_motor.stop(BRAKE)
    # brain.screen.print("xfinal: %.2f, y final: %.2f"%(x, y))
    # brain.screen.new_line()
    # brain.screen.print("s shape 2 end")




    # arc_points = 75
    # theta0 = np.pi / 2  # initial heading
    # x0 = radius_circle  # initial x
    # y0 = 0.0            # initial y

    # # Center of first arc (to the left of robot, radius away)
    # center1 = (x0 - radius_circle * np.sin(theta0), y0 + radius_circle * np.cos(theta0))
    # theta1 = np.linspace(theta0, theta0 + 1.5*np.pi, arc_points)
    # x1 = center1[0] + radius_circle * np.sin(theta1)
    # y1 = center1[1] - radius_circle * np.cos(theta1)

    # # End of first arc
    # end_x1 = x1[-1]
    # end_y1 = y1[-1]
    # end_theta1 = theta1[-1]

    # # Center for second arc: to the right of the end point, radius away
    # center2 = (end_x1 + radius_circle * np.sin(end_theta1), end_y1 - radius_circle * np.cos(end_theta1))
    # theta2 = np.linspace(end_theta1, end_theta1 - 1.5*np.pi, arc_points)
    # x2 = center2[0] - radius_circle * np.sin(theta2)
    # y2 = center2[1] + radius_circle * np.cos(theta2)

    # # Concatenate arcs
    # s_x = np.concatenate([x1, x2])
    # s_y = np.concatenate([y1, y2])

    # with open('desired_path.py', 'w') as f:
    #     f.write("waypoints = [\n")
    #     for x, y in zip(s_x, s_y):
    #         f.write(f"    ({x}, {y}),\n")
    #     f.write("]\n")

    # # Plot the trajectory
    # plt.figure(figsize=(8, 8))
    # plt.plot(x_traj, y_traj, label='Robot Path')
    # plt.plot(s_x, s_y, 'r--', label='Desired S Path')
    # plt.plot(x_traj[0], y_traj[0], 'x', markeredgewidth=2, label='Start Location')
    # plt.plot(x_traj[-1], y_traj[-1], 'o', markeredgewidth=2, label='End Location')
    # plt.xlabel('X position')
    # plt.ylabel('Y position')
    # plt.title('Differential Drive Robot Following a Circular Trajectory')
    # plt.legend()
    # plt.axis('equal')
    # plt.grid()
    # plt.show()



 
#============================set up controller ===========================================
 
controller = Controller(PRIMARY)
 
def controller_drive():
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("Program running...")
    brain.screen.new_line()
    brain.screen.print("Controller in action..")
 
    while True:
 
        # Exit on X button
        if controller.buttonX.pressing():
            stop_motors()
            return
 
        # Tank-style mixing
        forward = controller.axis3.position()
        turn = controller.axis1.position()
 
        left_speed = clamp_speed(forward - turn)
        right_speed = clamp_speed(forward + turn)
 
        left_motor.spin(FORWARD, left_speed, PERCENT)
        right_motor.spin(FORWARD, right_speed, PERCENT)
 
        wait(20, MSEC)

 
#=============================main====================================================
def main():
 
        # programSelector('straight_line')
        # programSelector('turnL')
        # programSelector('turnR')
        # programSelector('spin')
        testing_second_S()
        # testing_spin(velocity_values[7])
        # programSelector('house')
        
       
        

        # draw_menu()
        # renameSlot(1, "House")
        # renameSlot(2, "Straight line")
        # renameSlot(3, "Turn Left")
        # renameSlot(4, "Turn Right")
        # renameSlot(5, "Spin")
        # renameSlot(6, "V %d"%(velocity_values[4]))
        # renameSlot(7, "V %d"%(velocity_values[5]))
        # renameSlot(8, "V %d"%(velocity_values[6]))
        # renameSlot(9, "V %d"%(velocity_values[7]))
        
 
        # button = get_button()
 
        # if button == 1:
        #     programSelector('house')
        #     #testing_spin(velocity_values[0])
        # elif button == 2:
        #     programSelector('straight_line')
        #     #testing_spin(velocity_values[1])
        # elif button == 3:
        #     programSelector('turnL')
        # elif button == 4:
        #     programSelector('turnR')
        # elif button == 5:
        #     programSelector('spin')
        # elif button == 6:
        #     pass
        # elif button == 7:
        #     pass
        # elif button == 8:
        #     testing_spin(velocity_values[7])
        # elif button == 9:
        #     pass
 
main()