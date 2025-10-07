from sys import argv
from collections import defaultdict
import re
import itertools


def on_map(y: int, x: int, height: int, width: int) -> bool:
    return 0 <= y < height and 0 <= x < width


def get_antiodes(a: tuple[int, int], b: tuple[int, int]) -> list[tuple[int, int]]:
    ay, ax = a
    by, bx = b

    dy = abs(ay - by)
    dx = abs(ax - bx)

    if ay + dy == by:
        ay -= dy
        by += dy
    else:
        ay += dy
        by -= dy

    if ax + dx == bx:
        ax -= dx
        bx += dx
    else:
        ax += dx
        bx -= dx

    return [(ay, ax), (by, bx)]


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
        for a in get_antiodes(*pair):
            if on_map(*a, len(map), len(map[0])):
                antiodes.add(a)

print(len(antiodes))
