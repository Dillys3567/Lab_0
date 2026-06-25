from constants import *
from sensors import *
from part1_functions import *

# def move_in_s_shape_with_tracking_object_detection():
#     brain.screen.clear_screen()
#     brain.screen.set_cursor(1, 1)
#     brain.screen.print("moving in s shape while tracking position..")
#     brain.screen.new_line()
#     R = 50 # cm
#     theta_arc = 270
#     arc_time = 7.5 # s
#     arc_length = (2 * math.pi * R * theta_arc)/360
#     v = arc_length/arc_time
#     w = v/R
#     vl = v - (w * BASELINE/2)
#     vr = v + (w * BASELINE/2)
#     wl = abs(2*vl/DIAMETER)
#     wr = abs(2*vr/DIAMETER)
#     left_speed = clamp_speed_RPM(wl * 60/(2 * math.pi))
#     right_speed = clamp_speed_RPM(wr * 60/(2 * math.pi))

#     x = 100 # x start
#     y = 150 # y start
#     theta = math.pi/2

#     dt = 0.001

#     brain.screen.print("x_init: %.2f, y_init: %.2f, theta_init: %.2f"%(x, y, theta*180/math.pi))
#     brain.screen.new_line()

#     brain.timer.reset()
#     start_time = brain.timer.time(SECONDS)

#     total_time = 2 * arc_time
#     object_detected = False
#     break_time = 0
#     total_break_time = 0

#     while brain.timer.time(SECONDS) - start_time < total_time:
#         object_detected = is_object_close()
        
#         if object_detected:
#             time_at_detection = brain.timer.time(SECONDS)
#             brain.screen.print("Object detected! Stopping the robot.")
#             stop_motors()

#             while is_object_close():
#                 pass

#             break_time = brain.timer.time(SECONDS) - time_at_detection
        
#         elapsed = brain.timer.time(SECONDS) - start_time - break_time
#         total_time += break_time
#         total_break_time += break_time
#         break_time = 0

#         if elapsed < arc_time - TIME_CORRECTION:
#             w_arc = w
#             left_motor_speed = right_speed
#             right_motor_speed = left_speed
#         else:
#             w_arc = -w
#             left_motor_speed = left_speed
#             right_motor_speed = right_speed

#         left_motor.spin(FORWARD, left_motor_speed, RPM)
#         right_motor.spin(FORWARD, right_motor_speed, RPM)

#         x += v * math.cos(theta) * dt
#         y += v * math.sin(theta) * dt
#         theta += w_arc * dt

#         wait(dt, SECONDS)

#     left_motor.stop(BRAKE)
#     right_motor.stop(BRAKE)
#     stop_time = brain.timer.time(SECONDS)
#     run_time = stop_time - start_time + total_break_time
#     brain.screen.print("x_end: %.2f, y_end: %.2f, theta_end: %.2f"%(x, y, theta*180/math.pi))
#     brain.screen.new_line()
#     brain.screen.print("run time =  %.2f"%(run_time))
#     brain.screen.new_line()
#     brain.screen.print("s shape 2 end")
#     wait(20, SECONDS)


# def move_in_s_shape_with_tracking_object_detection():
#     brain.screen.clear_screen()
#     brain.screen.set_cursor(1, 1)
#     brain.screen.print("moving in s shape while detecting objects..")
#     brain.screen.new_line()
#     R = 50 # cm
#     theta_arc = 270
#     arc_time = 7.5 # s
#     arc_length = (2 * math.pi * R * theta_arc)/360
#     v = arc_length/arc_time
#     w = v/R
#     vl = v - (w * BASELINE/2)
#     vr = v + (w * BASELINE/2)
#     wl = abs(2*vl/DIAMETER)
#     wr = abs(2*vr/DIAMETER)
#     left_speed = clamp_speed_RPM(wl * 60/(2 * math.pi))
#     right_speed = clamp_speed_RPM(wr * 60/(2 * math.pi))

#     x = 100 # x start
#     y = 150 # y start
#     theta = math.pi/2

#     dt = 0.008

#     brain.screen.print("x_init: %.2f, y_init: %.2f, theta_init: %.2f"%(x, y, theta*180/math.pi))
#     brain.screen.new_line()


#     total_time = 2 * arc_time
#     object_detected = False

#     t=0
#     start_time = brain.timer.time(SECONDS)
#     while t <= total_time+0.3:
#         object_detected = is_object_close()
        
#         if object_detected:
#             stop_motors()
#             brain.screen.print("Object detected! Stopping the robot.")
#             while is_object_close():
#                 pass

#         if t < arc_time:
#             w_arc = w
#             left_motor_speed = right_speed
#             right_motor_speed = left_speed
#         else:
#             w_arc = -w
#             left_motor_speed = left_speed
#             right_motor_speed = right_speed

#         left_motor.spin(FORWARD, left_motor_speed, RPM)
#         right_motor.spin(FORWARD, right_motor_speed, RPM)

#         x += v * math.cos(theta) * dt
#         y += v * math.sin(theta) * dt
#         theta += w_arc * dt

#         wait(dt, SECONDS)
#         t += dt

#     left_motor.stop(BRAKE)
#     right_motor.stop(BRAKE)
#     stop_time = brain.timer.time(SECONDS)
#     run_time = stop_time - start_time 
#     brain.screen.print("x_end: %.2f, y_end: %.2f, theta_end: %.2f"%(x, y, theta*180/math.pi))
#     brain.screen.new_line()
#     brain.screen.print("run time =  %.2f"%(run_time))
#     brain.screen.new_line()
#     brain.screen.print("s shape 2 end")
#     wait(20, SECONDS)


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


    total_time = 2 * arc_time
    object_detected = False

    t=0
    start_time = brain.timer.time(SECONDS)
    while t <= total_time+0.55:
        object_detected = is_object_close()
        
        if object_detected:
            stop_motors()
            while is_object_close():
                pass

        if t < arc_time:
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
        t += dt

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

            


