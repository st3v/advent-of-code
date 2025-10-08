from sys import argv
import re
from math import lcm

with open(argv[1]) as file:
    turns, nodes = file.read().strip().split("\n\n")
    turns = turns.strip()

    network = {}
    for node in nodes.split("\n"):
        matches = re.findall(r"([A-Z0-9]+)\s=\s\(([A-Z0-9]+)\,\s([A-Z0-9]+)\)", node)
        if matches:
            name, left, right = matches[0]
            network[name] = (left, right)

current = set([n for n in network if n[-1] == "A"])
ending = set([n for n in network if n[-1] == "Z"])

steps = [0 for _ in range(len(current))]
for i, c in enumerate(current):
    steps[i] = 0
    while c not in ending:
        if turns[steps[i] % len(turns)] == "L":
            c = network[c][0]
        else:
            c = network[c][1]
        steps[i] += 1

print(lcm(*steps))  # least common multiple
