from constants import *
def padText(text):
    text = text[:MAXCHARS]
    padding = MAXCHARS - len(text)
 
    left = padding // 2
    right = padding - left
 
    result = " " * left + text + " " * right
    return result
 
 
def draw_menu():
    brain.screen.clear_screen()
    for row in range(NROWS):
        for col in range(NCOLS):
            x = SCREEN_X0 + col * (BUTTON_W + SPACING_W)
            y = SCREEN_Y0 + row * (BUTTON_H + SPACING_H)
 
            brain.screen.draw_rectangle(x, y, BUTTON_W, BUTTON_H)
 
            number = row * 3 + col + 1
            brain.screen.print_at(padText("Button " + str(number)), x=x+SPACING_W, y=y+CHAR_SPACING_Y + SPACING_H/2)
 
def renameButton(slotNumber, newName):
    slotIndex = slotNumber -1
    if slotIndex not in range(NROWS*NCOLS): 
       return
    row = slotIndex // NCOLS
    col = slotIndex % NCOLS
    x = SCREEN_X0 + col * (BUTTON_W + SPACING_W) + SPACING_W
    y = SCREEN_Y0 + row * (BUTTON_H + SPACING_H) + CHAR_SPACING_Y + SPACING_H/2
    brain.screen.print_at(padText(newName), x=x, y=y)
 
 
 
def get_button():
    while not brain.screen.pressing():
        wait(20, MSEC)

    x = brain.screen.x_position()
    y = brain.screen.y_position()

    while brain.screen.pressing():
        wait(20, MSEC)

    # convert to coordinates relative to menu origin
    x -= SCREEN_X0
    y -= SCREEN_Y0

    cell_w = BUTTON_W + SPACING_W
    cell_h = BUTTON_H + SPACING_H

    col = x // cell_w
    row = y // cell_h

    # outside grid
    if col < 0 or col >= NCOLS or row < 0 or row >= NROWS:
        return None

    # return none if inside a spacing region
    if x % cell_w > BUTTON_W:
        return None

    if y % cell_h > BUTTON_H:
        return None

    return row * NCOLS + col + 1


