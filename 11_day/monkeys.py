import os
import numpy as np


class Monkey:

    def __init__(self,
                 description,
                 reduce_worry='naive'):
        self.__parse_description(description)
        self.reduce_worry = reduce_worry
        self.inspections = 0
        

    def __parse_description(self, description):
        description = description.split('\n')
        self.name = description[0][-2]
        inventory = description[1].split('Starting items: ')[-1]
        inventory = [int(x) for x in inventory.split(', ')]
        self.inventory = inventory

        operation = description[2]
        self.__parse_operation(operation)
        test = description[3:]
        self.__parse_test(test)

    def __parse_operation(self, operation):
        operator, value = operation.split()[-2:]
        if not operator in ['+', '*']:
            raise ValueError(f'Operator {operator} not implemented!')
        if value == 'old':
            if operator == '+':
                self.operation = lambda x: x + x
            elif operator == '*':
                self.operation = lambda x: x * x
        else:
            if operator == '+':
                self.operation = lambda x: x + int(value)
            elif operator == '*':
                self.operation = lambda x: x * int(value)

    def __parse_test(self, test_str):
        test, true, false = test_str
        div_tester = int(test.split().pop())
        self.div_tester = div_tester
        true_target = int(true.split().pop())
        false_target = int(false.split().pop())

        def test_function(input):
            if input % div_tester == 0:
                return true_target
            else:
                return false_target

        self.test = test_function
    
    def add_item(self, item):
        self.inventory.append(item)

    def take_turn(self):
        out = []
        items = len(self.inventory)
        for i in range(items):
            item = self.inventory.pop(0)
            item = self.operation(item)
            if self.reduce_worry == 'naive':
                item = item // 3
            else:
                item = item % self.reduce_worry
            out.append((item, self.test(item))) 
            self.inspections += 1
        return out
    
    def __str__(self):
        out = f"I'm monkey {self.name}. I have items {self.inventory}. "
        out += f"I've inspected {self.inspections} times."
        return out

monkeys = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""
dirpath = os.path.dirname(__file__)
input_path = os.path.join(dirpath, "input")
with open(input_path, "r") as f:
    monkeys = f.read()
monkeys_str = monkeys[:-1].split('\n\n')

# part 1
monkeys = [Monkey(x) for x in monkeys_str]

for round in range(20):
    for monkey_idx in range(len(monkeys)):
        items_to_move = monkeys[monkey_idx].take_turn()
        for item, target in items_to_move:
            monkeys[target].add_item(item)
print('Monkey situation: ')
[print(x) for x in monkeys]
monkeysort = sorted(monkeys, key=lambda x: -x.inspections)
score = monkeysort[0].inspections * monkeysort[1].inspections
print(f'Monkey business score: {score}')

# part 2
reduce_worry = np.prod([x.div_tester for x in monkeys])  
monkeys = [Monkey(x, reduce_worry) for x in monkeys_str]

for round in range(10000):
    for monkey_idx in range(len(monkeys)):
        items_to_move = monkeys[monkey_idx].take_turn()
        for item, target in items_to_move:
            monkeys[target].add_item(item)
monkeysort = sorted(monkeys, key=lambda x: -x.inspections)
score = monkeysort[0].inspections * monkeysort[1].inspections
print(f'Monkey business score: {score}')