import os
import numpy as np


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


# part 2
def get_edge_points(sensor):
    d = sensor['distance']
    sx, sy = sensor['location']
    out = np.empty((2 + (2 * d + 1) * 2, 2), dtype=int)
    out[-2, :] =  (sx, sy+d+1)
    out[-1, :] =  (sx, sy-d-1)
    i = 0
    for dy in range(-d, d+1):
        dx = abs(abs(dy) - d) + 1
        out[i, :] = (sx + dx, sy + dy)
        out[i+1, :] = (sx - dx, sy + dy)
        i += 2
    return out



def point_in_sensor(point, sensor, limits=(0, 4000000)):
    in_x_lim = point[0] >= limits[0] and point[0] <= limits[1]
    if not in_x_lim:
        return True
    in_y_lim = point[1] >= limits[0] and point[1] <= limits[1]
    if not in_y_lim:
        return True
    out = distance(point, sensor['location']) <= sensor['distance']
    return out


beacon_point = None
i = 0
num_sensors = len(sensors)
for sensor in sensors:
    edge_points = get_edge_points(sensor)
    print(f'Check sensor {i+1}/{num_sensors} ({len(edge_points)} to check).')
    
    for point in edge_points:
        if all(not point_in_sensor(point, x) for x in sensors if x != sensor):
            beacon_point = point
            break
    i += 1
    if beacon_point is not None:
        break

part2_distress_signal = beacon_point[0] * 4e6 + beacon_point[1]
print(f'Beacon tuning frequency is {int(part2_distress_signal)}')