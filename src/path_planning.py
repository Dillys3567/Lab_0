
from astar import *
from constants import *

def update_grid_with_obstacle(grid, row, column, robot_radius, cell_size):
    inflate = math.ceil(robot_radius / cell_size)

    for i in range(-inflate, inflate + 1):
        for j in range(-inflate, inflate + 1):

            # Circular inflation OR immediate diagonals
            if math.sqrt(i*i + j*j) <= inflate or (abs(i) == 1 and abs(j) == 1):

                nr = row + i
                nc = column + j

                if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
                    grid[nr][nc] = 1

def add_obstacles(grid,obstacles,robot_radius, cell_size):
    for obstacle in obstacles:
        update_grid_with_obstacle(grid,obstacle[0],obstacle[1],robot_radius, cell_size)


def path_planning():

    d_tiles = 100/3  #cm

    grid = [
    # C0 C1 C2 C3 C4 C5
    [0, 0, 0, 0, 0, 0],  # R0
    [0, 0, 0, 0, 0, 0],  # R1
    [0, 0, 0, 0, 0, 0],  # R2
    [0, 0, 0, 0, 0, 0],  # R3
    [0, 0, 0, 0, 0, 0],  # R4
    [0, 0, 0, 0, 0, 0]  # R5
    ]

    obstacles = [
        [3,2],
        [0,5],
        [1,2],
    ]
   
    add_obstacles(grid,obstacles,ROBOT_RADIUS,d_tiles)
   

    start = (0, 0)
    goal = (5, 5)

    path = astar(grid, start, goal)

    if path == []:
        stop_motors(COAST)
        brain.screen.clear_screen()
        brain.screen.set_cursor(1,1)
        brain.screen.print("No path found")
        print("No path found")
        brain.screen.new_line()
        wait(5, SECONDS)
        while True:
            pass

    print("Path found:")
    print(path)

    
    distance_unit = d_tiles #* 1.5
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
    k_omega = 2.5

    # Time parameters
    dt = 0.007  # Time step
    total_time = 1000  # Total simulation time
    close_enough = 0.5 # How close is close enough to a waypoint?

    # Initial robot state (position and orientation)
    x = 0.0
    y = 0.0
    theta = 0.0

    # Define the trajectory (waypoints)

    
    waypoints = [[(x + 0.5)*distance_unit for x in row] for row in path]

    next_wp_ind = 0

    # Simulate the robot following the trajectory
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    print("planning trajectory...")
    brain.screen.print("planning trajectory...")
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
    brain.screen.print("At goal")
    brain.screen.new_line()
    wait(5, SECONDS)
    