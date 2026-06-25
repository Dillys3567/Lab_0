from constants import *

def is_object_close(distance=DISTANCE_THRESHOLD):
    if distance_sensor.object_distance(MM) < distance*10:
        return True
    return False

def configure_optical_sensor():
    optical_sensor.set_light(LedStateType.OFF)
    # optical_sensor.set_light_power(100, PERCENT)


def sense_colour():
    hue = optical_sensor.hue()
    if hue > 31 and hue < 35:
        return "yellow"
    elif hue > 80 and hue < 150:
        return "green"
    elif hue > 0 and hue < 15:
        return "red"
    elif hue > 345 and hue <= 359:
        return "red"
    elif hue > 185 and hue < 220:
        return "blue"
    else:
        return None

