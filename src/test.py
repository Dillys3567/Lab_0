
import math
from astar import *


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

grid = [
# C0 C1 C2 C3 C4 C5
[0, 0, 0, 0, 0, 0],  # R0
[0, 0, 0, 0, 0, 0],  # R1
[0, 0, 0, 0, 0, 0],  # R2
[0, 0, 0, 0, 0, 0],  # R3
[0, 0, 0, 0, 0, 0],  # R4
[0, 0, 0, 0, 0, 0],  # R5
]
obstacles = [
        [3,2],
        [0,5],
        [1,2],
        [0,0]
    ]
   
add_obstacles(grid,obstacles,24,100/3)


start = (0, 0)
goal = (5, 5)

path = astar(grid, start, goal)

if path == []:
    # stop_motors(COAST)
    # brain.screen.print("No path found")
    print("No path found")
    # brain.screen.new_line()
    # wait(5, SECONDS)
    while True:
        pass

print("Path found:")
print(path)