import numpy as np
import heapq
import string
import os


class Vertex:

    def __init__(self, char, height, coords, is_start=False):
        self.char = char
        self.height = height
        self.coords = coords
        self.distance = np.inf
        self.predecessor = None
        self.is_start = is_start

    def set_distance(self, distance):
        self.distance = distance
        return self.distance

    def set_predecessor(self, predecessor):
        self.predecessor = predecessor
        return self.predecessor

    def __str__(self):
        return str(self.char)

    def __repr__(self):
        return str(self.char)

    def __lt__(self, other):
        if self.coords[0] != other.coords[0]:
            return self.coords[0] < other.coords[0]
        else:
            return self.coords[1] < other.coords[1]


grid_str = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""
dirpath = os.path.dirname(__file__)
input_path = os.path.join(dirpath, 'input')
with open(input_path, 'r') as f:
    grid_str = f.read()
grid_str = grid_str.split('\n')[:-1]
height_map = {c: n for n, c in enumerate(string.ascii_lowercase)}
height_map['S'] = 0
height_map['E'] = len(string.ascii_lowercase) - 1

rows = len(grid_str)
cols = len(grid_str[0])
grid = np.empty((rows, cols), dtype=object)
for i in range(rows):
    if grid_str[i] != '':
        grid[i, :] = [Vertex(grid_str[i][j],
                             height_map[grid_str[i][j]],
                             (i, j))
                      for j in range(len(grid_str[i]))
                      if grid_str[i] not in ['', '\n']]

print(grid)


def get_neighbours(grid, i, j):
    max_i, max_j = grid.shape
    out = [None] * 4
    if (i != 0):
        out[0] = grid[i-1, j]
    if (i < max_i-1):
        out[1] = grid[i+1, j]
    if (j != 0):
        out[2] = grid[i, j-1]
    if (j < max_j-1):
        out[3] = grid[i, j+1]
    out = [x for x in out if x is not None]
    curr_height = grid[i, j].height
    out = [x for x in out if x.height <= curr_height + 1]
    return out


def find_optimal_path(grid, start_coords):
    # Basic Djikstra's algorithm with priority queue (= heapq)
    rows, cols = grid.shape
    visited = set()
    Q = []
    grid[start_coords].set_distance(0)
    heapq.heappush(Q, (0, grid[start_coords]))

    while Q:
        dist_u, u = heapq.heappop(Q)
        i, j = u.coords
        neighs = get_neighbours(grid, i, j)
        neighs = [v for v in neighs if v.coords not in visited]
        for v in neighs:
            alt = dist_u + 1
            if alt < v.distance:
                v.set_distance(alt)
                v.set_predecessor(u)
                heapq.heappush(Q, (v.distance, v))
            if v.char == 'E':
                return v.distance
        visited.add(u.coords)


# part 1
start_coords = np.unravel_index(np.where([x.char == 'S'
                                          for x in grid.flatten()])[0],
                                grid.shape)
start_coords = tuple([x[0] for x in start_coords])
print('Part 1 optimal path length: ' +
      f'{find_optimal_path(grid, start_coords)}')

# part 2
# loop over possible starts, choose smallest
start_coords = np.unravel_index(np.where([x.char == 'S' or x.char == 'a'
                                            for x in grid.flatten()]),
                                grid.shape)
start_coords = zip(start_coords[0][0], start_coords[1][0])
start_coords = [x for x in start_coords]
smallest_distance = np.Inf
for start in start_coords:
    distance = find_optimal_path(grid, start)
    if distance is not None and distance < smallest_distance:
        smallest_distance = distance
print(f'Part 2 optimal path length: {smallest_distance}')

