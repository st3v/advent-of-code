from sys import argv
from collections import defaultdict

connections = defaultdict(set)
for l in open(argv[1]):
    a, b = l.strip().split("-")
    connections[a].add(b)
    connections[b].add(a)

triplets = set()
for a, neighbors in connections.items():
    for b in neighbors:
        for c in neighbors & connections[b]:
            if "t" in [a[0], b[0], c[0]]:
                triplets.add(tuple(sorted([a, b, c])))

print(len(triplets))
