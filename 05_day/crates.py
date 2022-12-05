import os
from collections import defaultdict
from copy import deepcopy

# input
dirpath = os.path.dirname(__file__)
input_path = os.path.join(dirpath, 'input')
lines = []
with open(input_path, 'r') as f:
    lines = f.readlines()

# read inputs
crates = []
for line in lines:
    if line == '\n':
        break
    else:
        crates.append(line.replace('\n', ''))

stacks = defaultdict(list)
for crate_line in crates[:-1]:
    for i in range(9):
        if crate_line[1+4*i] != ' ':
            stacks[i].append(crate_line[1+4*i])

# reverse lists to make them into proper stacks
for k in stacks.keys():
    stacks[k].reverse()

# copy stack for safekeeping
init_stack = deepcopy(stacks)


def parse_move(move_str):
    words = move_str.split()
    amount = int(words[1])
    # move to zero-indexed world
    start = int(words[3]) - 1
    target = int(words[5]) - 1
    return amount, start, target


moves = [parse_move(x) for x in lines if x[0] == 'm']

# part 1
# just treat the stacks as stacks :D
for amount, start, target in moves:
    for i in range(amount):
        to_move = stacks[start].pop()
        stacks[target].append(to_move)

top_crates = [stacks[k][-1] for k in range(9)]
print(f'Top crates are: {"".join(top_crates)}')

# part 2
# now we can move substacks
stacks = deepcopy(init_stack)
for amount, start, target in moves:
    to_move = stacks[start][-amount:]
    stacks[start] = stacks[start][:-amount]
    stacks[target] += to_move

top_crates = [stacks[k][-1] for k in range(9)]
print(f'Top crates for better machine are: {"".join(top_crates)}')
