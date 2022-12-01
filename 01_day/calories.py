import os

# input
dirpath = os.path.dirname(__file__)
input_path = os.path.join(dirpath, 'input')
items = []
with open(input_path, 'r') as f:
   items = f.readlines()

items = [int(x.strip()) if x != '\n' else -1 for x in items]

# part 1
elf_calories = []
curr_calories = 0
max_calories = -1
for item in items:
    if item == -1:
        elf_calories.append(curr_calories)
        if curr_calories > max_calories:
            max_calories = curr_calories
        curr_calories = 0
    else:
        curr_calories += item

print(f'Max calories carried by elf: {max_calories}.')

# part 2

elf_calories = sorted(elf_calories, reverse=True)
top3 = elf_calories[:3]
print(f'Top 3 elves are carrying {top3} calories, total {sum(top3)}')
