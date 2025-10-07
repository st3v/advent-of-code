from sys import argv
from collections import defaultdict, deque

connections = defaultdict(set)
for l in open(argv[1]):
    a, b = l.strip().split("-")
    connections[a].add(b)
    connections[b].add(a)

ans = ""
max = 0
for a, neighbors in connections.items():
    q = deque(neighbors)

    group = {a}
    seen = {a}

    while q:
        nxt = q.pop()
        seen.add(nxt)
        if group & connections[nxt] != group:
            continue

        group.add(nxt)
        if len(group) + len(q) <= max:
            break

        for c in connections[nxt] - seen:
            q.append(c)

    if len(group) > max:
        max = len(group)
        ans = ",".join(sorted(group))

print(ans)
