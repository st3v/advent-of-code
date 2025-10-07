from sys import argv
import re
from collections import Counter
import math


def move(
    pos: tuple[int, int],
    steps_per_second: tuple[int, int],
    seconds: int,
    height: int,
    width: int,
) -> tuple[int, int]:
    x, y = pos
    dx, dy = steps_per_second
    ty = (y + dy * seconds) % height
    tx = (x + dx * seconds) % width
    return (tx, ty)


robots: list[tuple[tuple[int, int], tuple[int, int]]] = []
with open(argv[1], "r") as file:
    for line in file:
        parts = re.findall(
            "p=([0-9]*)\\,([0-9]*)\\sv=([\\-{0,1}0-9]*)\\,([\\-{0,1}0-9]*)",
            line.strip(),
        )

        if not parts or len(parts[0]) != 4:
            continue

        robots.append(
            ((int(parts[0][0]), int(parts[0][1])), (int(parts[0][2]), int(parts[0][3])))
        )

h, w = 103, 101
seconds = 100

counts: dict[tuple[int, int], int] = Counter()
for pos, steps in robots:
    x, y = move(pos, steps, seconds, h, w)
    counts[(x, y)] += 1


div_x = (w - 1) // 2
div_y = (h - 1) // 2
quadrants: dict[int, int] = Counter()

total = 0
for (x, y), n in counts.items():
    if x < div_x and y < div_y:
        quadrants[0] += n
    elif x < div_x and y > div_y:
        quadrants[1] += n
    elif x > div_x and y > div_y:
        quadrants[2] += n
    elif x > div_x and y < div_y:
        quadrants[3] += n

if not quadrants:
    total = 0
else:
    total = 1
    for _, n in quadrants.items():
        total *= n

print(len(robots))
print(total)
