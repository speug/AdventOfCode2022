import os
import string

# input
dirpath = os.path.dirname(__file__)
input_path = os.path.join(dirpath, 'input')
sacks = []
with open(input_path, 'r') as f:
    sacks = f.readlines()

sacks = [x.rstrip() for x in sacks]
# validate parity
print(all([len(x) % 2 == 0 for x in sacks]))

# part 1
# take intersection of sets of chars on right and left side => get wrong item
wrong_items = []
for sack in sacks:
    sack_size = len(sack)
    left = set(list(sack[:sack_size // 2]))
    right = set(list(sack[sack_size // 2:]))
    wrong_item = (left & right).pop()
    wrong_items.append(wrong_item)

lower_priorities = {char: prio+1 for prio, char in enumerate(string.ascii_lowercase)} 
upper_priorities = {char: prio+27 for prio, char in enumerate(string.ascii_uppercase)} 
priority_map = lower_priorities | upper_priorities
priorities = [priority_map[item] for item in wrong_items]
total_prio = sum(priorities)
print(f'Total priority of wrong items is {total_prio}')

# part 2
# split into groups of 3, do two consectutive intersections instead
groups = [sacks[i * 3:(i + 1) * 3] for i in range((len(sacks) + 3 - 1) // 3 )]
badges = []
for group in groups:
    one, two, three = [set(list(x)) for x in group]
    badge = (one & two & three).pop()
    badges.append(badge)

badge_prios = [priority_map[badge] for badge in badges]
total_prio = sum(badge_prios)
print(f'Total priority of badges is {total_prio}')