from constants import *
from astar import *


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

path = astar(grid, start, goal)
print(path)


# grid = [
#     [0,0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,1,0,1,1,1,0],
#     [0,1,1,1,1,0,0,0,1,0],
#     [0,0,1,0,1,0,0,0,1,0],
#     [0,0,1,0,1,0,1,0,1,0],
#     [0,0,1,1,1,1,1,1,1,0],
#     [0,0,0,0,0,0,0,0,0,0],
# ]

# start = (0, 0)
# goal = (6, 9)

# path = astar(grid, start, goal)

# print("Path found:")
# print(path)
    



def path_planning():
    d_tiles = 100/3  #cm
    distance_unit = d_tiles
    d_error_init = math.sqrt(2)* distance_unit
    theta_error_init = math.pi/4
    
    # Control gains
    # We will use p-control to set the linear &
    # angular velocities of the robot proportional to the errors
    # in positions and angles respectively
    w_ave= 1.85 #rad/s
    v_ave = 26.21#cm/s
    k_v_init = v_ave / d_error_init
    k_w_init = w_ave / theta_error_init

    k_v = 0.5
    k_omega = 2.38

    # Time parameters
    dt = 0.01  # Time step
    total_time = 1000  # Total simulation time
    close_enough = 0.5 # How close is close enough to a waypoint?

    # Initial robot state (position and orientation)
    x = 0.0
    y = 0.0
    theta = 0.0

    # Define the trajectory (waypoints)

    
    waypoints = [[(x+0.5)*distance_unit for x in row] for row in path]

    next_wp_ind = 0

    # Simulate the robot following the trajectory
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    print("Path Planning...")
    brain.screen.print("Path planning...")
    brain.screen.new_line()
    t = 0
    while t <= total_time:

        # if we are close enough to the next waypoint on the 
        # trajectory, move to the next waypoint
        waypoint_x = waypoints[next_wp_ind][0] 
        waypoint_y = waypoints[next_wp_ind][1] 
        dist_to_waypoint = math.sqrt((waypoint_x - x)**2 + (waypoint_y - y)**2)
        if (dist_to_waypoint < close_enough):
            next_wp_ind += 1
            brain.screen.print("At waypoint x=%.2f, y=%.2f"%(x,y))
            brain.screen.new_line()

        #Break if the robot has reached the final waypoint
        if (next_wp_ind >= len(waypoints)):
            break

        nearest_waypoint = waypoints[next_wp_ind]
        
        # Compute the control inputs
        distance = math.sqrt((nearest_waypoint[0] - x)**2 + (nearest_waypoint[1] - y)**2)
        angle_to_target = math.atan2(nearest_waypoint[1] - y, nearest_waypoint[0] - x)
        angle_error = angle_to_target - theta

    

        # Normalize angle error to be within -pi to pi
        angle_error = (angle_error + math.pi) % (2 * math.pi) - math.pi
        # print("theta: ",theta,  "angle error: ", angle_error * 180/math.pi, "distance: ", distance)
        
        # Compute linear and angular velocities
        # basically using p control for velocity control
        # -- we are making the target velocity proportional to the error
        v = k_v * distance
        w = k_omega * angle_error

    
    
        vl = v - (w * BASELINE/2)
        vr = v + (w * BASELINE/2)
        wl = 2*vl/DIAMETER
        wr = 2*vr/DIAMETER


        # TO DO
        # limit the wheel velocities to "allowable" values based on
        # robot constraints and control the wheels.
        left_speed = clamp_speed_RPM(wl * 60/(2 * math.pi),100)
        right_speed = clamp_speed_RPM(wr * 60/(2 * math.pi),100)

        spin_right_motor(right_speed)
        spin_left_motor(left_speed)


        # Update robot's position and orientation
        x += v * math.cos(theta) * dt
        y += v * math.sin(theta) * dt
        theta += w * dt
        t = t+dt
        wait(dt, SECONDS)

    stop_motors(COAST)
    brain.screen.print("end of trajectory")
    brain.screen.new_line()
    wait(5, SECONDS)


# def update_grid_with_obstacle(grid, ox, oy, robot_radius, cell_size):
#     inflate = math.ceil(robot_radius / cell_size)

#     r, c = world_to_grid(ox, oy)

#     for i in range(-inflate, inflate + 1):
#         for j in range(-inflate, inflate + 1):

#             if math.sqrt(i*i + j*j) <= inflate:

#                 nr = r + i
#                 nc = c + j

#                 if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
#          
#            grid[nr][nc] = 1