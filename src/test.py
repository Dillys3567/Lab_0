from constants import *
from sensors import *

def test_optical_sensor():
    brain.screen.clear_screen()
    brain.screen.set_cursor(1,1)
    brain.screen.print("Testing optical sensor...")
    configure_optical_sensor()
    while True:
        colour = sense_colour()
        if colour:
            print(colour)
        else:
            print("none")
        wait(0.3, SECONDS)