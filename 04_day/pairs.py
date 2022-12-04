import os

# input
dirpath = os.path.dirname(__file__)
input_path = os.path.join(dirpath, 'input')
pairs = []
with open(input_path, 'r') as f:
    pairs = f.readlines()

pairs = [x.rstrip().split(',') for x in pairs]
pairs = [(a.split('-'), b.split('-')) for a, b in pairs]

# part 1
def contains_range(range_1, range_2, debug=False):
    """Check if range 1 contains range 2."""
    out = range_1[0] <= range_2[0] and range_1[1] >= range_2[1]
    if debug:
        if out:
            print(f'Found contained ranges: {range_2} ⊆ {range_1}')
    return out 

contained_pairs = 0
for a, b in pairs:
    a = [int(x) for x in a]
    b = [int(x) for x in b]
    if contains_range(a, b) or contains_range(b, a):
        contained_pairs += 1

print(f'Total contained pairs: {contained_pairs}')

# part 2:
def overlaps_range(range_1, range_2):
    out = range_1[0] <= range_2[0] and range_1[1] >= range_2[0]
    return out

overlapping_pairs = 0
for a, b in pairs:
    a = [int(x) for x in a]
    b = [int(x) for x in b]
    if overlaps_range(a, b) or overlaps_range(b, a):
        overlapping_pairs += 1

print(f'Total overlapping pairs: {overlapping_pairs}')