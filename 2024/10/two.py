from sys import argv
from collections import defaultdict
import copy


def on_map(row: int, col: int, height: int, width: int) -> bool:
    return 0 <= row < height and 0 <= col < width


def rating(
    prev: int,
    x: int,
    y: int,
    height: int,
    width: int,
    topo: list[list[int]],
    visited: dict[int, dict[int, bool]],
) -> int:
    if not on_map(x, y, height, width) or visited[x][y]:
        return 0

    if topo[x][y] - prev != 1:
        return 0

    visited[x][y] = True

    if topo[x][y] == 9:
        return 1

    total = 0
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        total += rating(
            topo[x][y], x + dx, y + dy, height, width, topo, copy.deepcopy(visited)
        )

    return total


topo: list[list[int]] = []
trailheads: list[tuple[int, int]] = []
with open(argv[1], "r") as file:
    for i, line in enumerate(file):
        row = list(map(int, line.strip()))
        topo.append(row)
        for j, t in enumerate(row):
            if t == 0:
                trailheads.append((i, j))

height, width = len(topo), len(topo[0])

total = 0
for hx, hy in trailheads:
    visited: dict[int, dict[int, bool]] = defaultdict(lambda: defaultdict(bool))
    total += rating(-1, hx, hy, height, width, topo, visited)

print(total)
