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


from menu import *
from part1_functions import *
from part2_functions import *



    

#=============================main====================================================
def main():
 
  while(1):

    draw_menu() # menu has 9 buttons

    # rename buttons
    renameButton(1, "200cm line")
    renameButton(2, "Turn Left")
    renameButton(3, "Turn Right")
    renameButton(4, "Spin 90L")
    renameButton(5, "Spin 90R")
    renameButton(6, "House Shape")
    renameButton(7, "S path 1")
    renameButton(8, "S path 2")

    

    button = get_button()

    if button == 1:
        programSelector('straight_line')
    elif button == 2:
        programSelector('turnL')
    elif button == 3:
        programSelector('turnR')
    elif button == 4:
        programSelector('spinL')
    elif button == 5:
        programSelector('spinR')
    elif button == 6:
        programSelector('house')
    elif button == 7:
        move_in_s_shape()
    elif button == 8:
        move_in_s_shape_with_tracking()
    elif button == 9:
        NOPROGRAM(9)
        # pass
 
main()