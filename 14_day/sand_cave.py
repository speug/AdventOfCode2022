import numpy as np
import os

cave = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""
dirpath = os.path.dirname(__file__)
input_path = os.path.join(dirpath, 'input')
with open(input_path, 'r') as f:
    cave = f.read()


def generate_all_points_between(prev, curr):
    x_sign = 1 if np.sign(curr[0] - prev[0]) == 1 else -1
    y_sign = 1 if np.sign(curr[1] - prev[1]) == 1 else -1
    out = []
    for x in range(prev[0], curr[0] + x_sign, x_sign):
        for y in range(prev[1], curr[1] + y_sign, y_sign):
            out.append((x, y))
    return out


cave = cave.split('\n')[:-1]
rock_coords = []
sand_coords = []
for c_l in cave:
    endpoints = c_l.split(' -> ')
    endpoints = [ep.split(',') for ep in endpoints]
    endpoints = [(int(x[0]), int(x[1])) for x in endpoints]
    curr = endpoints[0]
    for i in range(1, len(endpoints)):
        rock_coords += generate_all_points_between(curr, endpoints[i])
        curr = endpoints[i]

# part 1
# keep track of occupied coords in a hash table
rock_coords.append((500, 0))
cols = max([x[0] for x in rock_coords]) - min([x[0] for x in rock_coords]) + 1
x_off = min([x[0] for x in rock_coords])
rows = max([x[1] for x in rock_coords]) + 1
rock_coords = rock_coords[:-1]
# dictionary is a hash table, so search is O(1)
occupied_coords = {(k[0] - x_off, k[1]): 0 for k in rock_coords}


def check_if_free(coords, floor=False):
    if coords in occupied_coords:
        return False
    elif coords[1] == rows + 1 and floor:
        return False
    return True


sand_full = False
sand_particles = 0
while not sand_full:
    sand_coords = (500 - x_off, 0)
    stopped = False
    while not stopped:
        if sand_coords[1] == rows - 1:
            sand_full = True
            break
        if check_if_free((sand_coords[0], sand_coords[1] + 1)):
            sand_coords = (sand_coords[0], sand_coords[1] + 1)
        elif check_if_free((sand_coords[0] - 1, sand_coords[1] + 1)):
            sand_coords = (sand_coords[0] - 1, sand_coords[1] + 1)
        elif check_if_free((sand_coords[0] + 1, sand_coords[1] + 1)):
            sand_coords = (sand_coords[0] + 1, sand_coords[1] + 1)
        else:
            stopped = True
            occupied_coords[sand_coords] = 0
            sand_particles += 1
print(f'Sand particles: {sand_particles}')

# part 2
# much of the same, but add floor to above function

occupied_coords = {(k[0] - x_off, k[1]): 0 for k in rock_coords}
sand_particles = 0
while not (500 - x_off, 0) in occupied_coords:
    sand_coords = (500 - x_off, 0)
    stopped = False
    while not stopped:
        if check_if_free((sand_coords[0], sand_coords[1] + 1), True):
            sand_coords = (sand_coords[0], sand_coords[1] + 1)
        elif check_if_free((sand_coords[0] - 1, sand_coords[1] + 1),
                           True):
            sand_coords = (sand_coords[0] - 1, sand_coords[1] + 1)
        elif check_if_free((sand_coords[0] + 1, sand_coords[1] + 1),
                           True):
            sand_coords = (sand_coords[0] + 1, sand_coords[1] + 1)
        else:
            stopped = True
            occupied_coords[sand_coords] = 0
            sand_particles += 1

print(f'Part 2 sand particles: {sand_particles}')
