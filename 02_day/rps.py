import os
import numpy as np
from enum import Enum


class Throw(Enum):
    ROCK = 0
    PAPER = 1
    SCISSORS = 2


opponent_rolls = {
    'A': Throw.ROCK,
    'B': Throw.PAPER,
    'C': Throw.SCISSORS
}

guide_rolls = {
    'X': Throw.ROCK,
    'Y': Throw.PAPER,
    'Z': Throw.SCISSORS
}

# input
dirpath = os.path.dirname(__file__)
input_path = os.path.join(dirpath, 'input')
guide = []
with open(input_path, 'r') as f:
    guide = f.readlines()

guide = [x.rstrip().split() for x in guide]


def rps(opponent, player):
    """
    Play RPS.
    The game can be seen as a matrix with opponent rolls as rows
    and player rolls as columns. Each element is then the player
    score for the game. As the game is cyclical, all we need to do
    is to rotate the first row and pick the appropriate element.
    Matrix form:
           player    R   P   S
        opp
        R            3   6   0
        P            0   3   6
        S            6   0   3
    """
    scores = np.array([3, 6, 0])
    scores = np.roll(scores, opponent.value)
    return scores[player.value]


def score_round(opponent, player):
    outcome_score = rps(opponent, player)
    outcome_score += player.value + 1
    return outcome_score


# part 1
part1_guide = [(opponent_rolls[x[0]], guide_rolls[x[1]]) for x in guide]
scores = [score_round(opp, player) for opp, player in part1_guide]
total = sum(scores)
print(f'Part 1 total score: {total}.')

# part 2
# now need to map to desired outcomes


def match_outcome(opponent_throw, desired_outcome):
    # codify the outcome matrix from above
    # find the desired outcome by index
    # create a matching throw
    match_matrix = np.array([
        [3, 6, 0],
        [0, 3, 6],
        [6, 0, 3]])
    match_row = match_matrix[opponent_throw.value, :]
    throw_val = np.where(match_row == desired_outcome)[0][0]
    return Throw(throw_val)


def secret_strategy(opponent, outcome):
    player = match_outcome(opponent, outcome)
    return score_round(opponent, player)


outcome_map = {
    'X': 0,
    'Y': 3,
    'Z': 6
}

part2_guide = [(opponent_rolls[x[0]], outcome_map[x[1]]) for x in guide]
scores = [secret_strategy(opp, outcome) for opp, outcome in part2_guide]
total = sum(scores)
print(f'Part 2 total score: {total}.')
