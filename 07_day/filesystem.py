import os
from abc import ABC, abstractmethod

class FSEntry(ABC):

    def __init__(self,
                 name,
                 parent,
                 is_dir,
                 is_root,
                 size=None):
        self.name = name
        self.parent = parent
        self.is_root = is_root
        self.path = self.name + self.parent.path if not self.is_root else self.name
        self.is_dir = is_dir
        self.size = size

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
                 parent,
                 is_root=False):
        super().__init__(name, parent, is_root=is_root, is_dir=True)
        self.contents = []

    def get_size(self):
        return sum([x.get_size() for x in self.contents])

    def add_contents(self, to_add):
        if any(x.path == to_add.path for x in self.contents):
            raise ValueError(f'Entry {to_add} already_exists in {self}!')
        self.contents.append(to_add)

    def __str__(self):
        out = self.get_depth() * '  ' + self.name + '/\n'
        for con in self.contents:
            out += con.__str__()
        return out

class File(FSEntry):
    def __init__(self,
                 name,
                 parent,
                 size):
        super().__init__(name, parent, is_root=False, is_dir=False, size=size)

    def get_size(self):
        return self.size

    def __str__(self):
        out = self.get_depth() * '  ' + self.name + '\n'
        return out

# testing
test_input = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""

root = Directory('/', None, is_root=True)
pointer = root
append_mode = False
for line in test_input.split('\n')[1:]:
    if line[:4] == '$ cd':
        target = line.split('$ cd ')[1]
        if target == '..':
            pointer = pointer.parent
        else:
            pointer = next(x for x in pointer.contents if x.name == target)
    elif line == '$ ls':
        continue
    else:
        preamble, name = line.split()
        if preamble == 'dir':
            new_dir = Directory(name=name, parent=pointer, is_root=False)
            pointer.add_contents(new_dir)
        else:
            new_file = File(name=name, parent=pointer, size=int(preamble))
            pointer.add_contents(new_file)

print(str(root))
print(root.get_size())

