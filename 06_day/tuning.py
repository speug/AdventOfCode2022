import os

# input
dirpath = os.path.dirname(__file__)
input_path = os.path.join(dirpath, "input")
with open(input_path, "r") as f:
    stream = f.read()

stream = stream.rstrip()


def find_first_n_nunique(string, n):
    for i in range(len(stream) - n):
        sub = set(stream[i:i + n])
        if len(sub) == n:
            return i
    return -1


# part 1

print("Packet start marker begins at index " +
      f"{find_first_n_nunique(stream, 4) + 4}")

# part 2
# the same, but now we need 14 chars
print("Message start marker begins at index " +
      f"{find_first_n_nunique(stream, 14) + 14}")
