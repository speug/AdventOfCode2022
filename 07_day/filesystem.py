import os
from abc import ABC, abstractmethod


class FSEntry(ABC):

    def __init__(self,
                 name,
                 is_dir,
                 is_root,
                 size=None,
                 parent=None):
        self.name = name
        self.parent = parent
        self.is_root = is_root
        self.is_dir = is_dir
        self.size = size

    def path(self):
        if self.is_root:
            return self.name
        if not self.parent:
            return self.name
        return self.name + self.parent.path

    def __repr__(self):
        return self.path

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def get_size(self):
        pass

    def get_depth(self):
        if self.is_root:
            return 0
        else:
            return self.parent.get_depth() + 1


class Directory(FSEntry):

    def __init__(self,
                 name,
                 is_root=False):
        super().__init__(name, is_root=is_root, is_dir=True)
        self.contents = []

    def get_size(self):
        return sum([x.get_size() for x in self.contents])

    def add_contents(self, to_add):
        if any(x.path == to_add.path for x in self.contents):
            raise ValueError(f'Entry {to_add} already_exists in {self}!')
        self.contents.append(to_add)
        to_add.parent = self

    def __str__(self):
        out = (
            self.get_depth() * '  ' + self.name +
            '/' * (not self.is_root) + '\n')
        for con in self.contents:
            out += con.__str__()
        return out

    def get_small_subdirs(self, result=None, size_threshold=100000):
        if result is None:
            result = []
        if self.get_size() < size_threshold:
            result.append((self.name, self.get_size()))
        subdirs = [x for x in self.contents if x.is_dir]
        [x.get_small_subdirs(result) for x in subdirs]
        return result

    def get_subdirs(self, result=None):
        if result is None:
            result = []
        result.append((self.name, self.get_size()))
        subdirs = [x for x in self.contents if x.is_dir]
        [x.get_subdirs(result) for x in subdirs]
        return result


class File(FSEntry):
    def __init__(self,
                 name,
                 size):
        super().__init__(name, is_root=False, is_dir=False, size=size)

    def get_size(self):
        return self.size

    def __str__(self):
        out = self.get_depth() * '  ' + self.name + '\n'
        return out


def generate_filesystem(commands):
    root = Directory('/', is_root=True)
    pointer = root
    for line in commands:
        if line == '':
            continue
        elif line == '$ ls':
            continue
        if line[:4] == '$ cd':
            target = line.split('$ cd ')[1]
            if target == '..':
                # move one dir up
                pointer = pointer.parent
            else:
                # find the correct subdir
                pointer = next(x for x in pointer.contents if x.name == target)
        else:
            preamble, name = line.split()
            if preamble == 'dir':
                new_dir = Directory(name=name, is_root=False)
                pointer.add_contents(new_dir)
            else:
                new_file = File(name=name, size=int(preamble))
                pointer.add_contents(new_file)
    return root


# assignment
dirpath = os.path.dirname(__file__)
input_path = os.path.join(dirpath, "input")
with open(input_path, "r") as f:
    real_input = f.read()

root = generate_filesystem(real_input.split('\n')[1:])
subdirs = root.get_subdirs()
small_subdirs = [x for x in subdirs if x[1] < 100000]
sum_small = sum([x[1] for x in small_subdirs])
print(f'Part 1: the sum of small subdirs is {sum_small}')
fs_size = 7e7
free_space_required = 3e7
space_to_be_freed = root.get_size() - (fs_size - free_space_required)
best_to_remove = min([x for x in subdirs if x[1] >= space_to_be_freed],
                     key=lambda x: x[1] - free_space_required)
print(f'Part 2: best to remove is {best_to_remove}')
