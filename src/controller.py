from constants import *
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
 
        left_speed = clamp_speed_percent(forward - turn)
        right_speed = clamp_speed_percent(forward + turn)
 
        left_motor.spin(FORWARD, left_speed, PERCENT)
        right_motor.spin(FORWARD, right_speed, PERCENT)
 
        wait(20, MSEC)