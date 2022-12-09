import os
import numpy as np


direction_map = {
    'U': np.array([0, 1]),
    'R': np.array([1, 0]),
    'D': np.array([0, -1]),
    'L': np.array([-1, 0])
}


def draw_debug(head_pos, tail_pos, start=[0, 0], grid_size=(26, 26)):
    grid = np.zeros(grid_size)
    try:
        grid[head_pos[1], head_pos[0]] = 1
    except IndexError:
        print('Head is out of the grid')
    for i in range(len(tail_pos)):
        try:
            grid[tail_pos[i][1], tail_pos[i][0]] = i + 2
        except IndexError:
            print(f'Tail link {i+1} is out of the grid')
    printable = np.chararray(grid_size)
    printable[grid == 0] = '.'
    printable[0, 0] = 's'
    for i in range(len(tail_pos) - 1):
        printable[grid == i+2] = f'{i+1}'
    printable[grid == len(tail_pos) + 1] = 'T'
    printable[grid == 1] = 'H'
    print(np.flipud(printable))
    return


def move_rope(direction, head_pos, tail_pos):
    # head moves tail, tail links act as heads for each other
    head_pos += direction_map[direction]
    tail_pos[0] = move_tail(head_pos, tail_pos[0])
    for i in range(1, len(tail_pos)):
        tail_pos[i] = move_tail(tail_pos[i-1], tail_pos[i])
    return head_pos, tail_pos


def move_tail(head_pos, link_pos):
    dx, dy = head_pos - link_pos
    # if distance in one coord is 2 and 1 in another, needs diagonal move
    if (abs(dx) + abs(dy) > 2):
        link_pos += np.array(
            [np.sign(dx), np.sign(dy)])
    # otherwise, just step towards the head
    elif abs(dx) > 1:
        link_pos[0] += np.sign(dx)
    elif abs(dy) > 1:
        link_pos[1] += np.sign(dy)
    return link_pos


def process_move(move, head_pos, tail_pos, travelled, debug=False):
    direction, steps = move.split()
    for i in range(int(steps)):
        head_pos, tail_pos = move_rope(direction, head_pos, tail_pos)
        travelled.add(tuple(tail_pos[-1]))
        if debug:
            draw_debug(head_pos, tail_pos)
    return head_pos, tail_pos


# input
dirpath = os.path.dirname(__file__)
input_path = os.path.join(dirpath, "input")
with open(input_path, "r") as f:
    moves = f.read()
moves = moves.split('\n')[:-1]

# part 1
head_pos = np.array([0, 0])
tail_pos = [np.array([0, 0])]
travelled = set()
for move in moves:
    head_pos, tail_pos = process_move(move, head_pos, tail_pos, travelled,
                                      debug=False)
print(f'Total spaces the tail travels is {len(travelled)}')

# part 2
head_pos = np.array([0, 0])
tail_pos = [np.array([0, 0]) for x in range(9)]
travelled = set()
for move in moves:
    head_pos, tail_pos = process_move(move, head_pos, tail_pos, travelled,
                                      debug=False)
print(f'Total spaces the tip of longer tail travels is {len(travelled)}')
