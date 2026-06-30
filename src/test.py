import math
from astar import *



# grid = [
# #    0  1  2  3  4  5  6  7  8  9 10 11
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 0
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 1
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 2
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 3
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 4
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 5
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 6
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 7
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 8
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 9
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 10
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 11
# ]


grid = [
#    0  1  2  3  4  5
    [0, 0, 1, 0, 0, 0],  # 0
    [1, 0, 1, 1, 1, 0],  # 1
    [0, 0, 1, 0, 1, 0],  # 2
    [1, 0, 0, 0, 1, 0],  # 3
    [0, 1, 1, 1, 0, 0],  # 4
    [0, 0, 0, 0, 0, 0],  # 5
]

start = (0, 0)
goal = (5, 5)

path = astar(grid, start, goal, )
print(path)


# d_tiles = 100/3  #cm
# distance_unit = d_tiles * 1.5
# d_error_init = math.sqrt(2)* distance_unit
# theta_error_init = math.pi/4

# # Control gains
# # We will use p-control to set the linear &
# # angular velocities of the robot proportional to the errors
# # in positions and angles respectively
# w_ave= 1.85 #rad/s
# v_ave = 26.21#cm/s
# k_v_init = v_ave / d_error_init # 0.37
# k_w_init = w_ave / theta_error_init # 0.355

# print(k_v_init, k_w_init)