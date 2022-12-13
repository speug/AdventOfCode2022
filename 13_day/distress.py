import ast
import os
from functools import cmp_to_key


def listify(left, right):
    if isinstance(left, list) and not isinstance(right, list):
        right = [right]
    elif not isinstance(left, list) and isinstance(right, list):
        left = [left]
    return left, right


def compare_elements(left, right):
    """Compare assignment elements.
       If inputs are ints, compare them directly.
       If one or both are lists, wrap either non-list input in a list
       and compare elements until a pair with different values is found
       or one of the lists ends. If one list runs out of elements, that
       list is considered to be smaller.

       Returns
       -------
       -1 if left < right
       0 if left == right
       1 if left > right
    """
    i = 0
    left, right = listify(left, right)
    while True:
        l = left[i] if i < len(left) else None
        r = right[i] if i < len(right) else None
        if l is None and r is None:
            # return from this stack frame and continue
            return 0
        if l is None and r is not None:
            # right list is longer
            return -1
        elif l is not None and r is None:
            # left list is longer
            return 1
        else:
            if l == r:
                # if elements are equal, move onto the next element
                i += 1
                continue
            if all(isinstance(x, int) for x in [l, r]):
                return -1 if l < r else 1
            else:
                comp = compare_elements(l, r)
                # if lower frame returned 0, move on to the next element
                if comp == 0:
                    i += 1
                    continue
                else:
                    return comp


dirpath = os.path.dirname(__file__)
input_path = os.path.join(dirpath, 'input')
with open(input_path, 'r') as f:
    lists = f.read()

# part 1
pair_lists = lists[:-1].split('\n\n')
part2_lists = []
sum_indices = 0
swap_indices = []
for i in range(len(pair_lists)):
    pair = pair_lists[i]
    left, right = pair.split('\n')
    left = ast.literal_eval(left)
    right = ast.literal_eval(right)
    part2_lists += [left, right]
    comp = compare_elements(left, right)
    if comp == -1:
        sum_indices += i + 1
print(f'Sum of correct pair indices is {sum_indices}')

# part 2
part2_lists += [[[2]], [[6]]]
part2_lists = sorted(part2_lists, key=cmp_to_key(compare_elements))
div1_index = part2_lists.index([[2]]) + 1
div2_index = part2_lists.index([[6]]) + 1
print(f'Decoder key is {div1_index * div2_index}')
