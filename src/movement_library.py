from vex import *
import math

brain = Brain()
controller = Controller(PRIMARY)

DIAMETER = 9.93
BASELINE = 29.4

left_motor = Motor(Ports.PORT1)
right_motor = Motor(Ports.PORT10)

left_motor.set_reversed(True)


def distance_to_degrees(distance):
    circumference = DIAMETER * math.pi
    return (distance * 360) / circumference


def clamp_speed_20(speed):
    if speed > 20:
        return 20
    elif speed < -20:
        return -20
    return speed


def clamp_speed(speed):
    if speed > 100:
        return 100
    elif speed < -100:
        return -100
    return speed


def stop_motors():
    left_motor.stop(BRAKE)
    right_motor.stop(BRAKE)


def stop_motor(motor):
    if motor == LEFT:
        left_motor.stop(BRAKE)
    elif motor == RIGHT:
        right_motor.stop(BRAKE)


def drive_straight(distance, speed):
    speed = clamp_speed_20(speed)
    degrees = distance_to_degrees(distance)

    left_motor.spin_for(FORWARD, degrees, DEGREES, speed, PERCENT, wait=False)
    right_motor.spin_for(FORWARD, degrees, DEGREES, speed, PERCENT, wait=True)

    stop_motors()


def drive_straight_100(distance, speed):
    speed = clamp_speed(speed)
    degrees = distance_to_degrees(distance)

    left_motor.spin_for(FORWARD, degrees, DEGREES, speed, PERCENT, wait=False)
    right_motor.spin_for(FORWARD, degrees, DEGREES, speed, PERCENT, wait=True)

    stop_motors()


def turn(turn_angle, speed, direction):
    speed = clamp_speed_20(speed)
    degrees = (2 * BASELINE * turn_angle) / DIAMETER

    if direction == RIGHT:
        stop_motor(LEFT)
        right_motor.spin_for(FORWARD, degrees, DEGREES, speed, PERCENT, wait=True)

    elif direction == LEFT:
        stop_motor(RIGHT)
        left_motor.spin_for(FORWARD, degrees, DEGREES, speed, PERCENT, wait=True)

    stop_motors()


def spin(angle, speed, direction):
    speed = clamp_speed(speed)
    degrees = (BASELINE * angle) / DIAMETER

    if direction == RIGHT:
        left_motor.spin_for(REVERSE, degrees, DEGREES, speed, PERCENT, wait=False)
        right_motor.spin_for(FORWARD, degrees, DEGREES, speed, PERCENT, wait=True)

    elif direction == LEFT:
        left_motor.spin_for(FORWARD, degrees, DEGREES, speed, PERCENT, wait=False)
        right_motor.spin_for(REVERSE, degrees, DEGREES, speed, PERCENT, wait=True)

    stop_motors()


def square_move(distance, speed, direction):
    for i in range(4):
        drive_straight(distance, speed)
        turn(90, speed, direction)


def house_move(distance, speed, direction):
    drive_straight(distance, speed)
    turn(90, speed, direction)
    drive_straight(distance, speed)
    turn(30, speed, direction)
    drive_straight(distance, speed)
    turn(120, speed, direction)
    drive_straight(distance, speed)
    turn(30, speed, direction)
    drive_straight(distance, speed)
    turn(90, speed, direction)


def pentagon(distance, speed, direction):
    for i in range(5):
        drive_straight(distance, speed)
        turn(78, speed, direction)


def controller_drive():
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("Controller in action..")

    while True:
        if controller.buttonX.pressing():
            stop_motors()
            return

        forward = controller.axis3.position()
        turn_value = controller.axis1.position()

        left_speed = clamp_speed(forward - turn_value)
        right_speed = clamp_speed(forward + turn_value)

        left_motor.spin(FORWARD, left_speed, PERCENT)
        right_motor.spin(FORWARD, right_speed, PERCENT)

        wait(20, MSEC)