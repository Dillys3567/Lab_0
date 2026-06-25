from constants import *
from part1_functions import drive_straight,spin
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
    theta = 270
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

        if elapsed < arc_time:
            w_arc = w
            left_motor_speed = right_speed
            right_motor_speed = left_speed
        else:
            w_arc = -w
            left_motor_speed = left_speed
            right_motor_speed = right_speed

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