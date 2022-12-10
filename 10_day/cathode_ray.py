import os

dirpath = os.path.dirname(__file__)
input_path = os.path.join(dirpath, "input")
with open(input_path, "r") as f:
    instructions = f.read()
instructions = instructions.split("\n")[:-1]


def draw_screen(screen):
    for i in range(6):
        print("".join(screen[i]))


def run_instructions(instructions, debug=False):
    cycles = 1
    x = 1
    adding = False
    instruction_idx = 0
    curr_instruction = None
    signal_strengths = {}
    screen = [["." for x in range(40)] for y in range(6)]
    while instruction_idx < len(instructions):
        if cycles == 20 or (cycles - 20) % 40 == 0:
            signal_strengths[cycles] = x
        screen_row = (cycles - 1) // 40
        screen_idx = (cycles - 1) % 40
        if screen_idx in [x - 1, x, x + 1]:
            screen[screen_row][screen_idx] = "#"
        curr_instruction = instructions[instruction_idx]
        if curr_instruction[:4] == "addx":
            command, value = curr_instruction.split()
            if adding:
                x += int(value)
                adding = False
                instruction_idx += 1
            else:
                adding = True
        else:
            instruction_idx += 1
        if debug:
            print(
                f"After cycle {cycles}, x={x}. "
                + f"Current instruction: {curr_instruction}."
            )
        cycles += 1
    return x, signal_strengths, screen


# part 1
_, signal_strengths, screen = run_instructions(instructions)
print(f"Signal strengths: {signal_strengths}.")
total_strength = sum([k * v for k, v in signal_strengths.items()])
print(f"Total: {total_strength}")

# part 2
draw_screen(screen)
