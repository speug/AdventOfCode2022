import os
import numpy as np
import time


# https://stackoverflow.com/a/47705495/7207392
def connect2(ends):
    d0, d1 = np.diff(ends, axis=0)[0]
    if np.abs(d0) > np.abs(d1):
        return np.c_[np.arange(ends[0, 0], ends[1,0] + np.sign(d0),
                               np.sign(d0), dtype=np.int32),
                     np.full(np.abs(d0)+1, ends[0, 1]) if d1==0 else
                     np.arange(ends[0, 1] * np.abs(d0) + np.abs(d0)//2,
                               (ends[0, 1] * np.abs(d0) + np.abs(d0)//2
                                + (np.abs(d0)+1) * d1),
                               d1, dtype=np.int32) // np.abs(d0)]
    else:
        return np.c_[np.full(np.abs(d1)+1, ends[0, 0]) if d0==0 else
                     np.arange(ends[0, 0] * np.abs(d1) + np.abs(d1)//2,
                               (ends[0, 0] * np.abs(d1) + np.abs(d1)//2 + (np.abs(d1)+1) * d0),
                               d0, dtype=np.int32) // np.abs(d1),
                     np.arange(ends[0, 1], ends[1,1] + np.sign(d1),
                               np.sign(d1), dtype=np.int32)]

def dch(points):
    # implement yourself if time allows
    ch = ConvexHull(points)
    n = len(ch.vertices)
    return np.concatenate([connect2(points[ch.vertices[[i, (i+1)%n]]])[:-1] for i in range(n)], axis=0)


def generate_sensor_pol(sensor):
    sensor_x, sensor_y = sensor['location']
    dist = sensor['distance']
    sensor_shape_points = [[sensor_x, sensor_y + dist],
                           [sensor_x + dist, sensor_y],
                           [sensor_x, sensor_y - dist],
                           [sensor_x - dist, sensor_y]]
    return np.concatenate([connect2(np.array([sensor_shape_points[i],
                                              sensor_shape_points[(i+1)%4]]))
                           for i in range(4)], axis=0)


def point_in_pol(point, polygon):
    if point in polygon:
        return True
    x_lims = [x for x in polygon if x[1] == point[1]]
    if not x_lims:
        return False
    x_min, x_max = [x[0] for x in x_lims]
    if point[0] < x_min or point[0] > x_max:
        return False
    y_lims = [x for x in polygon if x[0] == point[0]]
    if not y_lims:
        return False
    y_min, y_max = [x[1] for x in y_lims]
    if point[1] < y_min or point[1] > y_max:
        return False
    return True

def combine_polygons(pol_a, pol_b):
    to_add = np.array([x for x in pol_b if not point_in_pol(x, pol_a)])
    if to_add.size > 0:
        pol_a = np.append(pol_a, to_add, axis=0)
    return pol_a

def distance(point1, point2):
    return abs(point2[0]-point1[0]) + abs(point2[1]-point1[1])


def parse_sensor(sensor_line):
    sensor_line = sensor_line.split()
    sensor_x = int(sensor_line[2][2:-1])
    sensor_y = int(sensor_line[3][2:-1])
    sensor_loc = (sensor_x, sensor_y)
    beacon_x = int(sensor_line[-2][2:-1])
    beacon_y = int(sensor_line[-1][2:])
    beacon_loc = (beacon_x, beacon_y)
    dist = distance(sensor_loc, beacon_loc)
    return {'location': sensor_loc,
            'closest_beacon': beacon_loc,
            'distance': dist}

sensors = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
"""
dirpath = os.path.dirname(__file__)
input_path = os.path.join(dirpath, 'input')
with open(input_path, 'r') as f:
    sensors = f.read()
sensors = sensors.split('\n')[:-1]
sensors = [parse_sensor(x) for x in sensors]
print(sensors)

# part 1
target_row = 2000000
x_min, x_max = None, None
for sensor in sensors:
    sx, sy = sensor['location']
    d = sensor['distance']
    dx = d - distance((sx, sy), (sx, target_row))
    sx_min = sx-dx
    sx_max = sx+dx
    if x_min is None or sx_min < x_min:
        x_min = sx_min
    if x_max is None or sx_max > x_max:
        x_max = sx_max
print(f'Ensured points on row {target_row} : {x_max-x_min}')


def combine_ranges(ranges):
    out = []
    for start, end in sorted(ranges):
        if out and out[-1][1] >= start - 1:
            out[-1][1] = max(out[-1][1], end)
        else:
            out.append([start, end])
    return out

def check_row(row, x_lims):
    ranges = []
    for sensor in sensors:
        sx, sy = sensor['location']
        d = sensor['distance']
        dx = d - distance((sx, sy), (sx, row))
        if dx < 0:
            break
        sx_min = sx-dx
        sx_max = sx+dx
        ranges.append(sorted([sx_min, sx_max]))
    ranges = combine_ranges(ranges)
    print(ranges)
    return len(ranges) > 1


def check_col(col, valid_rows):
    ranges = []
    for sensor in sensors:
        sx, sy = sensor['location']
        d = sensor['distance']
        dy = d - distance((sx, sy), (col, sy))
        if dy < 0:
            break
        sy_min = sy-dy
        sy_max = sy+dy
        ranges.append([sy_min, sy_max])
    for i in range(len(valid_rows)):
        row = valid_rows[i]
        row_is_valid = True
        for r in ranges:
            r = sorted(r)
            if r[0] <= row and r[1] >= row:
                row_is_valid = False
                break
        if row_is_valid:
            return (row, col)
    return False


def point_in_sensor(point, sensor, limits=(0, 4000000)):
    in_x_lim = point[0] >= limits[0] and point[0] <= limits[1]
    if not in_x_lim:
        return True
    in_y_lim = point[1] >= limits[0] and point[1] <= limits[1]
    if not in_y_lim:
        return True
    out = distance(point, sensor['location']) < sensor['distance']
    if out:
        print(sensor)
        print(distance(point, sensor['location']))
    return out


from itertools import combinations
combs = combinations(sensors, 2)
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
beacon_point = None
for sa, sb in combs:
    la, lb = sa['location'], sb['location']
    ra, rb = sa['distance'], sb['distance']
    d = distance(la, lb)
    if d > (ra+rb):
        connector = (lb[0]-la[0], lb[1]-la[1])
        unit_connector = (connector[0] / d, connector[1] / d)
        print(unit_connector)
        candidate_points = []
        candidate_point = np.array(la) + (np.array(unit_connector) * (ra + 1))
        candidate_point = np.round(candidate_point)
        candidate_points.append(candidate_point)
        for x in [-1, 1]:
            for y in [-1, 1]:
                candidate_points.append(np.array([candidate_point[0]+x,
                                                  candidate_point[1]+y]))
        candidate_point2 = np.array(la) + (np.array(unit_connector) * (ra + 2))
        candidate_point2 = np.round(candidate_point2)
        for x in [-1, 1]:
            for y in [-1, 1]:
                candidate_points.append(np.array([candidate_point2[0]+x,
                                                  candidate_point2[1]+y]))

        candidate_point = np.array(lb) - (np.array(unit_connector) * (rb + 1))
        candidate_point = np.round(candidate_point)
        candidate_points.append(candidate_point)
        for x in [-1, 1]:
            for y in [-1, 1]:
                candidate_points.append(np.array([candidate_point[0]+x,
                                                  candidate_point[1]+y]))
        candidate_point2 = np.array(lb) - (np.array(unit_connector) * (rb + 2))
        candidate_point2 = np.round(candidate_point2)
        for x in [-1, 1]:
            for y in [-1, 1]:
                candidate_points.append(np.array([candidate_point2[0]+x,
                                                  candidate_point2[1]+y]))
        for point in candidate_points:
            if all(not point_in_sensor(point, x) for x in sensors):
                print(point)
                beacon_point = point
                break

part2_distress_signal = beacon_point[0] * 4e6 + beacon_point[1]
print(f'Beacon tuning frequency is {int(part2_distress_signal)}')

