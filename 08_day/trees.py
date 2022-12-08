import os
import numpy as np


def highest_tree_in_direction(grid, rotation):
    """Get highest tree in given rotation. Works only for square matrices."""
    grid = np.rot90(grid, rotation)
    max_i = grid.shape[0]
    top_trees = np.full_like(grid, fill_value=-1)
    for i in range(1, max_i):
        mask = np.where(grid[i-1, :] > top_trees[i-1, :])
        top_trees[i, :] = top_trees[i-1, :]
        top_trees[i, mask] = grid[i-1, mask]
    top_trees = np.rot90(top_trees, -rotation)
    return top_trees


def check_trees(grid, rotation):
    """Mark trees that do not have higher counterparts in given direction."""
    heights = highest_tree_in_direction(grid, rotation)
    trees = grid > heights
    return trees


# input
grid_str = """30373
25512
65332
33549
35390
"""
dirpath = os.path.dirname(__file__)
input_path = os.path.join(dirpath, "input")
with open(input_path, "r") as f:
    grid_str = f.read()
lines = grid_str.split('\n')
max_j = len(lines[0])
max_i = len(lines) - 1  # -1 needed to avoid empty final line
grid = np.zeros((max_i, max_j), dtype=int)
for i in range(max_i):
    grid[i, :] = [int(x) for x in lines[i]]

# part 1
highest_trees = np.dstack([check_trees(grid, k) for k in range(4)])
reduced = np.sum(highest_trees, axis=-1)
trees_with_view = np.sum(reduced > 0)
print(f'Amount of trees with view is {trees_with_view}')


# part 2
def count_trees(grid, rotation):
    """Count trees that are visible from each tree."""
    grid = np.rot90(grid, rotation)
    max_i, max_j = grid.shape
    # initialize optimal conditions in the direction (all trees until edge
    # visible)
    visible_trees = np.arange(max_i)
    visible_trees = np.tile(visible_trees, (max_j, 1)).T
    # remove rows one by one; if element is not yet the highest,
    # reduce seen trees by one
    for i in range(1, max_i):
        trees = check_trees(grid[i:, :], 0)
        visible_trees[i:, :] = visible_trees[i:, :] - np.logical_not(trees)
    visible_trees = np.rot90(visible_trees, -rotation)
    return visible_trees


seen_trees = np.dstack([count_trees(grid, k) for k in range(4)])
reduced = np.prod(seen_trees, axis=-1)
max_idx = np.unravel_index(np.argmax(reduced), grid.shape)
print(f'Max visibility is at {max_idx} (height {grid[max_idx]}.')
print(f'Scenic score for this is {reduced[max_idx]}.')
