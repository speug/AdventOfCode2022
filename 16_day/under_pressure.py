import os
from queue import SimpleQueue as Queue
from copy import deepcopy
from itertools import combinations

valves = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
"""


class Valve:

    def __init__(self,
                 name,
                 flow_rate):
        self.name = name
        self.flow_rate = flow_rate
        self.connections = set()

    def total_flow(self, t, t_max=30):
        return (30 - t) * self.flow_rate

    def add_connection(self, other):
        self.connections.add(other)

    def __str__(self):
        out = f'{self.name}: flow rate {self.flow_rate}, '
        out += f'connections to {[x.name for x in self.connections]}'
        return out


def parse_valve(valve):
    valve = valve.split()
    name = valve[1]
    flow_rate = int(valve[4].split('=')[1][:-1])
    return Valve(name, flow_rate)


dirpath = os.path.dirname(__file__)
input_path = os.path.join(dirpath, 'input')
with open(input_path, 'r') as f:
    valves = f.read()
valve_lines = valves.split('\n')[:-1]
valves = [parse_valve(x) for x in valve_lines]
for valve in valve_lines:
    name = valve.split()[1]
    valve1 = next(x for x in valves if x.name == name)
    if 'valves' in valve:
        conn_names = valve.split('valves ')[-1].split(', ')
        for name in conn_names:
            valve2 = next(x for x in valves if x.name == name)
            valve1.add_connection(valve2)
            valve2.add_connection(valve1)

[print(x) for x in valves]


def find_path(start_name, end_name):
    # simple BFS
    q = Queue()
    explored = set(start_name)
    start = next(x for x in valves if x.name == start_name)
    q.put(start)
    links = dict()
    while not q.empty():
        v = q.get()
        if v.name == end_name:
            route = [v.name]
            prev = links[v]
            while prev != start:
                route.append(prev.name)
                prev = links[prev]
            return list(reversed(route))
        for w in v.connections:
            if w.name not in explored:
                explored.add(w.name)
                links[w] = v
                q.put(w)


valves_with_flow = [x for x in valves if x.flow_rate > 0]

# pregenerate all paths from one valve to others
route_pairs = combinations(valves_with_flow +
                           [next(x for x in valves if x.name == 'AA')], 2)
routes = {(x.name, y.name): find_path(x.name, y.name) for x, y in route_pairs}
route_pairs = combinations(valves_with_flow +
                           [next(x for x in valves if x.name == 'AA')], 2)
routes2 = {(y.name, x.name): find_path(y.name, x.name) for x, y in route_pairs}
routes = {**routes, **routes2}

# part 1
def solve(situation, best_scenario):
    closed_valves = situation['closed_valves']
    current_time = situation['t']
    for valve in closed_valves:
        # move to valve
        path = routes[(situation['current_valve'].name, valve.name)]
        move_time = len(path)
        new_time = current_time +  move_time
        # open current valve
        new_time += 1
        if new_time > 30:
            continue
        # create new situation
        total_flow = situation['total_flow'] + valve.total_flow(new_time)
        new_situation = dict()
        new_situation['current_valve'] = valve
        new_situation['total_flow'] = total_flow
        new_situation['t'] = new_time
        new_situation['open_valves'] = situation['open_valves'] + [valve]
        new_situation['closed_valves'] = [x for x in valves_with_flow
                                          if x not in new_situation['open_valves']]
        if total_flow > best_scenario['total_flow']:
            best_scenario = deepcopy(new_situation)
        best_scenario = solve(new_situation, best_scenario)
    return best_scenario

initial_situation = {
    'current_valve': next(x for x in valves if x.name == 'AA'),
    'total_flow': 0,
    't': 0,
    'open_valves': [],
    'closed_valves': valves_with_flow
}

best_scenario = solve(initial_situation, initial_situation)
print(f"Best case pressure relief: {best_scenario['total_flow']}")

def greedy_solve(situation, best_scenario):
    closed_valves = situation['closed_valves']
    current_time = situation['t']
    best_valve = None
    for valve in closed_valves:
        # find best valve
        # move to valve
        path = routes[(situation['current_valve'].name, valve.name)]
        move_time = len(path)
        new_time = current_time +  move_time
        # open current valve
        new_time += 1
        if new_time > 30:
            continue
        # create new situation
        total_flow = situation['total_flow'] + valve.total_flow(new_time)
        if best_valve is None or best_valve['total_flow'] < total_flow:
            best_valve = {'valve': valve,
                          'total_flow': total_flow,
                          'new_time': new_time}

    new_situation = dict()
    new_situation['current_valve'] = best_valve['valve']
    new_situation['total_flow'] = best_valve['total_flow']
    new_situation['t'] = best_valve['new_time']
    new_situation['open_valves'] = situation['open_valves'] + [new_situation['current_valve']]
    new_situation['closed_valves'] = [x for x in valves_with_flow
                                      if x not in new_situation['open_valves']]
    if best_valve['total_flow'] > best_scenario['total_flow']:
        best_scenario = deepcopy(new_situation)
    best_scenario = solve(new_situation, best_scenario)
    return best_scenario

best_scenario = greedy_solve(initial_situation, initial_situation)
print(f"Best case pressure relief (greedy): {best_scenario['total_flow']}")
