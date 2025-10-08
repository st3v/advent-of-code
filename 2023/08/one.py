from sys import argv
import re

with open(argv[1]) as file:
    turns, nodes = file.read().strip().split("\n\n")
    turns = turns.strip()

    network = {}
    for node in nodes.split("\n"):
        matches = re.findall(r"([A-Z]+)\s=\s\(([A-Z]+)\,\s([A-Z]+)\)", node)
        if matches:
            name, left, right = matches[0]
            network[name] = (left, right)

steps = 0
current = "AAA"
while current != "ZZZ":
    nxt = turns[steps % len(turns)]
    current = network[current][0] if nxt == "L" else network[current][1]
    steps += 1

print(steps)
