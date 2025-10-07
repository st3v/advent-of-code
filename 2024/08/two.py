from sys import argv
from collections import defaultdict
import re
import itertools


def on_map(y: int, x: int, height: int, width: int) -> bool:
    return 0 <= y < height and 0 <= x < width


def get_antiodes(
    a: tuple[int, int], b: tuple[int, int], height: int, width: int
) -> list[tuple[int, int]]:
    ay, ax = a
    by, bx = b

    dy = ay - by
    dx = ax - bx

    y, x = ay, ax
    res: set[tuple[int, int]] = set()
    while on_map(y, x, height, width):
        res.add((y, x))
        y += dy
        x += dx

    y, x = ay, ax
    while on_map(y, x, height, width):
        res.add((y, x))
        y -= dy
        x -= dx

    return list(res)


map: list[list[str]] = []
antennas: dict[str, list[tuple[int, int]]] = defaultdict(list)
with open(argv[1], "r") as file:
    for y, line in enumerate(file):
        map.append(list(line.strip()))
        for x, c in enumerate(line.strip()):
            if re.fullmatch("[A-Za-z0-9]", c):
                antennas[c].append((y, x))

antiodes: set[tuple[int, int]] = set()
for k, positions in antennas.items():
    for pair in itertools.combinations(positions, 2):
        for a in get_antiodes(*pair, len(map), len(map[0])):
            antiodes.add(a)

print(len(antiodes))
