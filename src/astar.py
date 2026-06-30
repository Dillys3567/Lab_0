# 29th June 2026.  Ayorkor Korsah
# Code generated with the assistance of ChatGPT
# A simple implementation of A* with Euclidean costs
from heapq_vex import *
import math

# ------------------------------------------------------
# A* WITH EUCLIDEAN COSTS
# ------------------------------------------------------

# 8-connected movement
DIRECTIONS = [
    (-1, 0),   # up
    (1, 0),    # down
    (0, -1),   # left
    (0, 1),    # right
    (-1, -1),  # up-left
    (-1, 1),   # up-right
    (1, -1),   # down-left
    (1, 1)     # down-right
]


def euclidean(a, b):
    return math.sqrt(
        (a[0] - b[0])**2 +
        (a[1] - b[1])**2
    )


def reconstruct_path(came_from, current):

    path = [current]

    while current in came_from:
        current = came_from[current]
        path.append(current)

    path.reverse()
    return path


def astar(grid, start, goal):

    rows = len(grid)
    cols = len(grid[0])

    open_set = []

    heappush(open_set, (0, start))

    came_from = {}

    g_score = {start: 0.0}

    open_hash = {start}



    while open_set:

        result = heappop(open_set)
        if result == []:
            break

        f, current = result

        if current not in open_hash:
            continue

        open_hash.remove(current)

        if current == goal:
            return reconstruct_path(came_from, current)

        for dr, dc in DIRECTIONS:

            neighbor = (current[0] + dr, current[1] + dc)
            r, c = neighbor

            if not (0 <= r < rows and 0 <= c < cols):
                continue

            if grid[r][c] == 1:
                continue

            movement_cost = euclidean(current, neighbor)

            tentative_g = g_score[current] + movement_cost

            if neighbor not in g_score or tentative_g < g_score[neighbor]:

                came_from[neighbor] = current
                g_score[neighbor] = tentative_g

                f_score = tentative_g + euclidean(neighbor, goal)

                heappush(open_set, (f_score, neighbor))
                open_hash.add(neighbor)
    return []

    